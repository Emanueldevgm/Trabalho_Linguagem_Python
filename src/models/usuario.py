                       
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from src.models.base import Base
import bcrypt

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    senha_hash = Column(String(255), nullable=False)
    perfil = Column(String(20), default="operador")                   
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    def definir_senha(self, senha_plana: str):
        """Gera hash da senha e armazena."""
        self.senha_hash = bcrypt.hashpw(senha_plana.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verificar_senha(self, senha_plana: str) -> bool:
        """Verifica se a senha fornecida confere com o hash."""
        return bcrypt.checkpw(senha_plana.encode('utf-8'), self.senha_hash.encode('utf-8'))

    def __repr__(self):
        return f"<Usuario {self.username}>"