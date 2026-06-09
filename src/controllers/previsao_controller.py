                                        
import pandas as pd
import joblib
import os
import numpy as np
from typing import Optional, List
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from datetime import datetime, timedelta
from src.models.contratos import ModeloIA
from src.repositories.venda_repo import VendaRepositorio
from src.models.previsao import Previsao
from src.utils.database import obter_session
from src.utils.excecoes import DadosInsuficientesError, ModeloNaoTreinadoError
from src.utils.decoradores import log_execucao


class ModeloPrevisaoDemanda(ModeloIA):
    """Implementação concreta de IA usando Random Forest (regressão)."""

    def __init__(self) -> None:
        self.modelo: Optional[RandomForestRegressor] = None
        self.dados_treino: Optional[pd.DataFrame] = None
        self.features: Optional[List[str]] = None

    def _preparar_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Cria features temporais: dia da semana, mês, dia do ano, etc."""
        df = df.copy()
        df['data'] = pd.to_datetime(df['data'])
        df['dia_semana'] = df['data'].dt.dayofweek
        df['mes'] = df['data'].dt.month
        df['dia_ano'] = df['data'].dt.dayofyear
        df['dia_mes'] = df['data'].dt.day
        df['lag_1'] = df['quantidade'].shift(1)
        df['lag_7'] = df['quantidade'].shift(7)
        df['media_7'] = df['quantidade'].rolling(7).mean()
        df = df.dropna()
        return df

    def treinar(self, dados_historicos: pd.DataFrame) -> None:
        if len(dados_historicos) < 14:
            raise DadosInsuficientesError(0, 14, len(dados_historicos))
        df = self._preparar_features(dados_historicos)
        self.features = ['dia_semana', 'mes', 'dia_ano', 'dia_mes', 'lag_1', 'lag_7', 'media_7']
        X = df[self.features]
        y = df['quantidade']
        self.modelo = RandomForestRegressor(n_estimators=100, random_state=42)
        self.modelo.fit(X, y)
        self.dados_treino = df

    def calcular_metricas(self, dados_historicos: pd.DataFrame) -> dict:
        if self.modelo is None or self.features is None:
            raise ModeloNaoTreinadoError()
        df = self._preparar_features(dados_historicos)
        X = df[self.features]
        y_true = df['quantidade']
        y_pred = self.modelo.predict(X)
        return {
            'rmse': float(np.sqrt(mean_squared_error(y_true, y_pred))),
            'mae': float(mean_absolute_error(y_true, y_pred))
        }

    def prever(self, passos_futuros: int) -> pd.DataFrame:
        if self.modelo is None or self.dados_treino is None:
            raise ModeloNaoTreinadoError()
        ultima_data = self.dados_treino['data'].max()
        previsoes = []
        dados_atuais = self.dados_treino.copy()
        for i in range(passos_futuros):
            data_previsao = ultima_data + timedelta(days=i + 1)
                                                                             
            nova_linha = {
                'data': data_previsao,
                'dia_semana': data_previsao.weekday(),
                'mes': data_previsao.month,
                'dia_ano': data_previsao.timetuple().tm_yday,
                'dia_mes': data_previsao.day,
                'lag_1': dados_atuais['quantidade'].iloc[-1] if not dados_atuais.empty else 0,
                'lag_7': dados_atuais['quantidade'].iloc[-7] if len(dados_atuais) >= 7 else 0,
                'media_7': dados_atuais['quantidade'].iloc[-7:].mean() if len(dados_atuais) >= 7 else 0
            }
            X_new = pd.DataFrame([nova_linha])[self.features]
            pred = self.modelo.predict(X_new)[0]
            previsoes.append({
                'data_previsao': data_previsao,
                'quantidade_prevista': max(0, int(round(pred)))
            })
                                                                       
            nova_linha['quantidade'] = pred
            dados_atuais = pd.concat([dados_atuais, pd.DataFrame([nova_linha])], ignore_index=True)
        return pd.DataFrame(previsoes)

    def salvar_modelo(self, caminho: str) -> None:
        if self.modelo and self.dados_treino is not None:
            joblib.dump({
                'modelo': self.modelo,
                'features': self.features,
                'dados_treino': self.dados_treino
            }, caminho)
        else:
            raise ModeloNaoTreinadoError()

    def carregar_modelo(self, caminho: str) -> None:
        if os.path.exists(caminho):
            dados = joblib.load(caminho)
            self.modelo = dados['modelo']
            self.features = dados['features']
            self.dados_treino = dados['dados_treino']
        else:
            raise FileNotFoundError(f"Arquivo {caminho} não encontrado.")


class PrevisaoController:
    def __init__(self):
        self.venda_repo = VendaRepositorio()
        self.modelo = ModeloPrevisaoDemanda()

    @log_execucao
    def gerar_previsao(self, produto_id: int, dias_futuros: int = 30) -> tuple[pd.DataFrame, dict]:
                                             
        historico = self.venda_repo.obter_historico_por_produto(produto_id, dias=90)
        if len(historico) < 14:
            raise DadosInsuficientesError(produto_id, 14, len(historico))

        caminho_modelo = f"models/modelo_previsao_produto_{produto_id}.pkl"
        if os.path.exists(caminho_modelo):
            self.modelo.carregar_modelo(caminho_modelo)
        else:
                                                    
            self.modelo.treinar(historico)

        metricas = self.modelo.calcular_metricas(historico)

                        
        previsao_df = self.modelo.prever(dias_futuros)

                                                     
        data_inicio = previsao_df['data_previsao'].min().date()
        data_fim = previsao_df['data_previsao'].max().date()
        total_previsto = previsao_df['quantidade_prevista'].sum()

        with obter_session() as session:
            nova_previsao = Previsao(
                produto_id=produto_id,
                periodo_inicio=data_inicio,
                periodo_fim=data_fim,
                quantidade_prevista=total_previsto,
                modelo_usado="RandomForest"
            )
            session.add(nova_previsao)
            session.commit()

                                                           
        os.makedirs("models", exist_ok=True)
        self.modelo.salvar_modelo(f"models/modelo_previsao_produto_{produto_id}.pkl")

        return previsao_df, metricas