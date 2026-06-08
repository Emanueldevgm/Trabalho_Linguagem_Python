from pathlib import Path
from sqlalchemy import create_engine
from src.utils import database
from src.utils.database import Base
from src.controllers.inventario_controller import InventarioController

TEST_DB_PATH = Path("data/test_inventario.db")


def setup_module(module):
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()
    engine = create_engine(f"sqlite:///{TEST_DB_PATH}", echo=False)
    database.engine = engine
    database.SessionLocal.configure(bind=engine)
    Base.metadata.create_all(bind=engine)


def teardown_module(module):
    database.engine.dispose()
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()


def test_inventario_compras_vendas_e_recomendacoes():
    controller = InventarioController()
    produto = controller.cadastrar_produto(
        nome="Teste Integração",
        categoria="Geral",
        preco=5.0,
        estoque_inicial=2
    )

    recomendacoes = controller.recomendar_compra(incremento_pedido=0)
    assert any(item["produto"].id == produto.id for item in recomendacoes)

    venda = controller.registrar_venda(produto.id, quantidade=1, valor_total=5.0)
    assert venda.produto_id == produto.id
