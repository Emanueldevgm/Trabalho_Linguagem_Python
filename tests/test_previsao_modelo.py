import pandas as pd
from src.ia.modelo_previsao import ModeloPrevisaoDemanda


def test_modelo_previsao_treina_e_prevê():
    datas = pd.date_range("2026-01-01", periods=30, freq="D")
    df = pd.DataFrame({
        "data": datas,
        "quantidade": [10 + i for i in range(30)]
    })

    modelo = ModeloPrevisaoDemanda()
    modelo.treinar(df)
    metricas = modelo.calcular_metricas(df)

    assert "rmse" in metricas and metricas["rmse"] >= 0
    assert "mae" in metricas and metricas["mae"] >= 0

    previsao = modelo.prever(7)
    assert len(previsao) == 7
    assert list(previsao.columns) == ["data_previsao", "quantidade_prevista"]
