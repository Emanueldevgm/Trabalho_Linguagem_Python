# src/models/previsao.py
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float, Date, String
from sqlalchemy.sql import func
from src.models.base import Base

class Previsao(Base):
    __tablename__ = "previsoes"

    id = Column(Integer, primary_key=True, index=True)
    data_geracao = Column(DateTime(timezone=True), server_default=func.now())
    produto_id = Column(Integer, ForeignKey("produtos.id", ondelete="CASCADE"), nullable=False)
    periodo_inicio = Column(Date, nullable=False)
    periodo_fim = Column(Date, nullable=False)
    quantidade_prevista = Column(Float, nullable=False)
    modelo_usado = Column(String(100), default="RandomForest")