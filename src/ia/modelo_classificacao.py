import os
from typing import Optional, List

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.utils.excecoes import DadosInsuficientesError, ModeloNaoTreinadoError


class ModeloClassificadorDemanda:
    """Classificador de nível de demanda para produtos."""

    def __init__(self) -> None:
        self.pipeline: Optional[Pipeline] = None
        self.features: List[str] = [
            'media_7',
            'lag_1',
            'lag_7'
        ]
        self.classes: List[str] = []
        self.dados_treino: Optional[pd.DataFrame] = None

    def treinar(self, historico: pd.DataFrame) -> None:
        if len(historico) < 2:
            raise DadosInsuficientesError(0, 2, len(historico))

        df = historico.copy()
        df['data'] = pd.to_datetime(df['data'])
        df['media_7'] = df['quantidade'].rolling(7, min_periods=1).mean()
        df['lag_1'] = df['quantidade'].shift(1).fillna(0)
        df['lag_7'] = df['quantidade'].shift(7).fillna(0)
        df = df.dropna()

        if df.empty:
            raise DadosInsuficientesError(0, 2, 0)

        q1, q2 = np.quantile(df['quantidade'], [0.33, 0.66])
        df['classe_demanda'] = np.where(
            df['quantidade'] <= q1,
            'baixo',
            np.where(df['quantidade'] <= q2, 'medio', 'alto')
        )

        X = df[self.features]
        y = df['classe_demanda']

        self.pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
        ])
        self.pipeline.fit(X, y)
        self.classes = list(self.pipeline.classes_)
        self.dados_treino = df

    def prever(self, historico: pd.DataFrame) -> dict:
        if self.pipeline is None:
            raise ModeloNaoTreinadoError()

        df = historico.copy()
        df['data'] = pd.to_datetime(df['data'])
        df['media_7'] = df['quantidade'].rolling(7, min_periods=1).mean()
        df['lag_1'] = df['quantidade'].shift(1).fillna(0)
        df['lag_7'] = df['quantidade'].shift(7).fillna(0)
        df = df.dropna()

        if df.empty:
            raise DadosInsuficientesError(0, 2, 0)

        ultima_linha = df.iloc[-1]
        X_new = pd.DataFrame([ultima_linha[self.features]])

        classe_prevista = self.pipeline.predict(X_new)[0]
        probabilidades = self.pipeline.predict_proba(X_new)[0]

        return {
            'classe_prevista': str(classe_prevista),
            'probabilidades': {
                classe: float(prob)
                for classe, prob in zip(self.pipeline.classes_, probabilidades)
            }
        }

    def salvar_modelo(self, caminho: str) -> None:
        if self.pipeline is None:
            raise ModeloNaoTreinadoError()

        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        joblib.dump(self.pipeline, caminho)

    def carregar_modelo(self, caminho: str) -> None:
        if not os.path.exists(caminho):
            raise FileNotFoundError(f"Arquivo {caminho} não encontrado.")

        self.pipeline = joblib.load(caminho)
        self.classes = list(self.pipeline.classes_)
