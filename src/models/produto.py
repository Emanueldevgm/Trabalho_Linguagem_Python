# src/models/produto.py
from sqlalchemy import Column, Integer, String, Float
from src.models.base import Base

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    categoria = Column(String(50), nullable=False)
    preco_unitario = Column(Float, nullable=False) # pyright: ignore[reportUnknownVariableType]
    estoque_atual = Column(Integer, default=0)
    estoque_minimo = Column(Integer, default=5)
    lead_time_dias = Column(Integer, default=7)  # tempo para repor

    def calcular_ponto_pedido(self, demanda_media_diaria: float, estoque_seguranca: int) -> int:
        """Calcula o ponto de pedido com base na demanda e lead time."""
        demanda_lead_time = demanda_media_diaria * self.lead_time_dias
        return int(demanda_lead_time + estoque_seguranca) # type: ignore

    def alerta_estoque_baixo(self, ponto_pedido: int) -> bool:
        return self.estoque_atual <= ponto_pedido # pyright: ignore[reportReturnType]

    def __repr__(self):
        return f"<Produto {self.nome} (estoque={self.estoque_atual})>"