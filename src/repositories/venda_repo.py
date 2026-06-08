# src/repositories/venda_repo.py
from typing import List # pyright: ignore[reportUnusedImport]
from sqlalchemy import func # pyright: ignore[reportUnusedImport]
from src.models.venda import Venda
from src.repositories.repositorio_base import RepositorioBase
from src.utils.database import obter_session # pyright: ignore[reportUnusedImport]
import pandas as pd
from datetime import datetime, timedelta

class VendaRepositorio(RepositorioBase[Venda]):
    def __init__(self):
        super().__init__(Venda)

    def obter_historico_por_produto(self, produto_id: int, dias: int = 90) -> pd.DataFrame:
        """Retorna DataFrame com colunas 'data' e 'quantidade' para o produto."""
        with self._get_session() as session:
            data_limite = datetime.now() - timedelta(days=dias)
            vendas = session.query(Venda).filter(
                Venda.produto_id == produto_id,
                Venda.data >= data_limite
            ).order_by(Venda.data).all()
            dados = [{"data": v.data.date(), "quantidade": v.quantidade} for v in vendas] # pyright: ignore[reportUnknownVariableType]
            if not dados:
                return pd.DataFrame(columns=["data", "quantidade"])
            df = pd.DataFrame(dados) # pyright: ignore[reportUnknownArgumentType]
            # Agrupa por dia (caso haja múltiplas vendas no mesmo dia)
            df = df.groupby("data", as_index=False).sum()
            return df