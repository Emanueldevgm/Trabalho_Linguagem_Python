import pandas as pd

from src.ia.modelo_classificacao import ModeloClassificadorDemanda
from src.ia.modelo_sentimento import ModeloSentimentoFeedback


def test_modelo_classificacao_treinar_e_prever(tmp_path):
    datas = pd.date_range(start="2026-01-01", periods=30, freq="D")
    quantidades = [10, 12, 9, 11, 15, 18, 16, 14, 20, 21, 19, 22, 23, 25, 24, 26, 28, 27, 29, 31, 30, 33, 35, 34, 32, 36, 38, 37, 39, 40]
    historico = pd.DataFrame({"data": datas, "quantidade": quantidades})

    modelo = ModeloClassificadorDemanda()
    modelo.treinar(historico)

    resultado = modelo.prever(historico)
    assert resultado["classe_prevista"] in {"baixo", "medio", "alto"}
    assert isinstance(resultado["probabilidades"], dict)
    assert abs(sum(resultado["probabilidades"].values()) - 1.0) < 1e-6

    caminho = tmp_path / "modelo_classificacao.pkl"
    modelo.salvar_modelo(str(caminho))

    modelo_carregado = ModeloClassificadorDemanda()
    modelo_carregado.carregar_modelo(str(caminho))
    resultado_carregado = modelo_carregado.prever(historico)
    assert resultado_carregado["classe_prevista"] in {"baixo", "medio", "alto"}


def test_modelo_sentimento_treinar_e_analisar(tmp_path):
    modelo = ModeloSentimentoFeedback()
    modelo.treinar()

    resultado = modelo.analisar("O produto foi excelente e o atendimento foi rápido")
    assert resultado["sentimento"] in {"positivo", "negativo"}
    assert abs(sum(resultado["probabilidades"].values()) - 1.0) < 1e-6

    caminho = tmp_path / "modelo_sentimento.pkl"
    modelo.salvar_modelo(str(caminho))

    modelo_carregado = ModeloSentimentoFeedback()
    modelo_carregado.carregar_modelo(str(caminho))
    resultado_carregado = modelo_carregado.analisar("Não estou satisfeito com o suporte")
    assert resultado_carregado["sentimento"] in {"positivo", "negativo"}
    assert abs(sum(resultado_carregado["probabilidades"].values()) - 1.0) < 1e-6
