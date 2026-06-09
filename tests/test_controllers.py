from datetime import datetime, timedelta
from pathlib import Path
from sqlalchemy import create_engine
from src.models.venda import Venda
from src.utils import database
from src.utils.database import Base
from src.controllers.previsao_controller import PrevisaoController
from src.controllers.inventario_controller import InventarioController
from src.controllers.ia_controller import IAController

TEST_DB_PATH = Path("data/test_controllers.db")


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


def test_previsao_controller_cria_previsao_com_dois_registros():
    inventario = InventarioController()
    produto = inventario.cadastrar_produto(
        nome="Produto Teste",
        categoria="Geral",
        preco=15.0,
        estoque_inicial=10
    )

    inventario.registrar_venda(produto.id, quantidade=1, valor_total=15.0)
    with database.SessionLocal() as session:
        venda = Venda(
            produto_id=produto.id,
            quantidade=2,
            valor_total=30.0,
            data=datetime.now() - timedelta(days=1)
        )
        session.add(venda)
        session.commit()

    model_file = Path(f"models/modelo_previsao_produto_{produto.id}.pkl")
    if model_file.exists():
        model_file.unlink()

    previsao_controller = PrevisaoController()
    previsao_df, metricas = previsao_controller.gerar_previsao(produto.id, dias_futuros=5)

    assert not previsao_df.empty
    assert len(previsao_df) == 5
    assert metricas["rmse"] >= 0
    assert metricas["mae"] >= 0
    assert model_file.exists()
    model_file.unlink()


def test_ia_controller_classificacao_e_sentimento(tmp_path):
    inventario = InventarioController()
    produto = inventario.cadastrar_produto(
        nome="Produto IA",
        categoria="Geral",
        preco=20.0,
        estoque_inicial=20
    )

    inventario.registrar_venda(produto.id, quantidade=1, valor_total=20.0)
    with database.SessionLocal() as session:
        venda = Venda(
            produto_id=produto.id,
            quantidade=2,
            valor_total=40.0,
            data=datetime.now() - timedelta(days=1)
        )
        session.add(venda)
        session.commit()

    ia_controller = IAController()
    ia_controller._caminho_modelo_classificacao = str(tmp_path / "modelo_classificacao_demanda.pkl")
    ia_controller._caminho_modelo_sentimento = str(tmp_path / "modelo_sentimento_feedback.pkl")

    resultado_demanda = ia_controller.classificar_demanda(produto.id)
    assert resultado_demanda["classe_prevista"] in {"baixo", "medio", "alto"}
    assert abs(sum(resultado_demanda["probabilidades"].values()) - 1.0) < 1e-6

    resultado_sentimento = ia_controller.analisar_feedback("Produto excelente, gostei muito")
    assert resultado_sentimento["sentimento"] in {"positivo", "negativo"}
    assert abs(sum(resultado_sentimento["probabilidades"].values()) - 1.0) < 1e-6
    assert Path(ia_controller._caminho_modelo_classificacao).exists()
    assert Path(ia_controller._caminho_modelo_sentimento).exists()
