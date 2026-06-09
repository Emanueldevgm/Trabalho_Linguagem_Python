import os
from typing import Optional

import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

from src.utils.excecoes import ModeloNaoTreinadoError


class ModeloSentimentoFeedback:
    """Modelo simples de NLP para análise de sentimento de feedback."""

    def __init__(self) -> None:
        self.pipeline: Optional[Pipeline] = None
        self.textos_treino = [
            "Excelente produto e entrega rápida",
            "Adorei o atendimento e a qualidade",
            "Muito satisfeito com a compra",
            "Recomendo para todos",
            "Ótima experiência, voltarei a comprar",
            "Produto muito bom, vale a pena",
            "Péssimo atendimento, não recomendo",
            "Produto demorou a chegar e veio errado",
            "Fiquei insatisfeito com a qualidade",
            "Não gostei, quero devolução",
            "Experiência ruim, o suporte não ajudou",
            "O produto quebrou rápido"
        ]
        self.labels_treino = [
            "positivo",
            "positivo",
            "positivo",
            "positivo",
            "positivo",
            "positivo",
            "negativo",
            "negativo",
            "negativo",
            "negativo",
            "negativo",
            "negativo"
        ]

    def treinar(self) -> None:
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer()),
            ('classifier', LogisticRegression(max_iter=500, solver='liblinear'))
        ])
        self.pipeline.fit(self.textos_treino, self.labels_treino)

    def analisar(self, texto: str) -> dict:
        if self.pipeline is None:
            self.treinar()

        texto = texto.strip()
        if not texto:
            raise ValueError("O texto de feedback não pode ficar vazio.")

        classe = self.pipeline.predict([texto])[0]
        probabilidades = self.pipeline.predict_proba([texto])[0]
        classes = self.pipeline.classes_

        return {
            'texto': texto,
            'sentimento': str(classe),
            'probabilidades': {
                classes[0]: float(probabilidades[0]),
                classes[1]: float(probabilidades[1])
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
