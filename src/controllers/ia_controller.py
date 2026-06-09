import os
from typing import Any

import pandas as pd

from src.ia.modelo_classificacao import ModeloClassificadorDemanda
from src.ia.modelo_sentimento import ModeloSentimentoFeedback
from src.repositories.venda_repo import VendaRepositorio
from src.utils.excecoes import DadosInsuficientesError


class IAController:
    """Controller para funcionalidades de IA: classificação e NLP."""

    def __init__(self) -> None:
        self.venda_repo = VendaRepositorio()
        self.classificador = ModeloClassificadorDemanda()
        self.sentimento = ModeloSentimentoFeedback()
        self._caminho_modelo_classificacao = "models/modelo_classificacao_demanda.pkl"
        self._caminho_modelo_sentimento = "models/modelo_sentimento_feedback.pkl"

    def classificar_demanda(self, produto_id: int) -> dict[str, Any]:
        historico = self.venda_repo.obter_historico_por_produto(produto_id, dias=90)
        if len(historico) < 14:
            raise DadosInsuficientesError(produto_id, 14, len(historico))

        modelo_status = "carregado"
        if os.path.exists(self._caminho_modelo_classificacao):
            self.classificador.carregar_modelo(self._caminho_modelo_classificacao)
        else:
            self.classificador.treinar(historico)
            os.makedirs(os.path.dirname(self._caminho_modelo_classificacao), exist_ok=True)
            self.classificador.salvar_modelo(self._caminho_modelo_classificacao)
            modelo_status = "treinado"

        resultado = self.classificador.prever(historico)
        resultado["modelo_status"] = modelo_status
        return resultado

    def analisar_feedback(self, texto: str) -> dict[str, Any]:
        modelo_status = "carregado"
        if os.path.exists(self._caminho_modelo_sentimento):
            self.sentimento.carregar_modelo(self._caminho_modelo_sentimento)
        else:
            self.sentimento.treinar()
            os.makedirs(os.path.dirname(self._caminho_modelo_sentimento), exist_ok=True)
            self.sentimento.salvar_modelo(self._caminho_modelo_sentimento)
            modelo_status = "treinado"

        resultado = self.sentimento.analisar(texto)
        resultado["modelo_status"] = modelo_status
        return resultado
