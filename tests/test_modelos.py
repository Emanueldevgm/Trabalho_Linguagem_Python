import pandas as pd
from src.models.produto import Produto


def test_calcular_ponto_pedido():
    produto = Produto(
        nome="Teste",
        categoria="Geral",
        preco_unitario=10.0,
        estoque_atual=2,
        estoque_minimo=5,
        lead_time_dias=7
    )

    ponto = produto.calcular_ponto_pedido(demanda_media_diaria=2.0, estoque_seguranca=3)
    assert ponto == 17
    assert produto.alerta_estoque_baixo(ponto) is True


def test_alerta_estoque_baixo_falso():
    produto = Produto(
        nome="Produto2",
        categoria="Geral",
        preco_unitario=10.0,
        estoque_atual=20,
        estoque_minimo=5,
        lead_time_dias=7
    )
    assert produto.alerta_estoque_baixo(10) is False
