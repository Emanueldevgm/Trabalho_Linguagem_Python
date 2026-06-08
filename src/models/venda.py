# src/models/venda.py
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float
from sqlalchemy.sql import func
from src.models.base import Base

class Venda(Base):
    __tablename__ = "vendas"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id", ondelete="CASCADE"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    valor_total = Column(Float, nullable=False) # pyright: ignore[reportUnknownVariableType]

    def __repr__(self):
        return f"<Venda produto_id={self.produto_id} qtd={self.quantidade}>"