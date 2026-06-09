                                      
from typing import List, Generic, TypeVar, Type               
from sqlalchemy.orm import Session
from src.models.contratos import Repositorio
from src.utils.database import obter_session

ModelType = TypeVar('ModelType')

class RepositorioBase(Repositorio[ModelType]):
    """Implementação genérica de repositório usando SQLAlchemy."""
    def __init__(self, modelo_classe: Type[ModelType]):
        self.modelo_classe = modelo_classe

    def _get_session(self) -> Session:
        return obter_session()

    def adicionar(self, entidade: ModelType, session: Session | None = None) -> ModelType:
        if session is None:
            with self._get_session() as local_session:
                local_session.add(entidade)
                local_session.commit()
                local_session.refresh(entidade)
                return entidade

        session.add(entidade)
        session.flush()
        session.refresh(entidade)
        return entidade

    def obter_por_id(self, id: int, session: Session | None = None) -> ModelType | None:
        if session is None:
            with self._get_session() as local_session:
                return local_session.query(self.modelo_classe).filter_by(id=id).first()
        return session.query(self.modelo_classe).filter_by(id=id).first()

    def listar(self, session: Session | None = None) -> List[ModelType]:
        if session is None:
            with self._get_session() as local_session:
                return local_session.query(self.modelo_classe).all()
        return session.query(self.modelo_classe).all()

    def atualizar(self, entidade: ModelType, session: Session | None = None) -> ModelType:
        if session is None:
            with self._get_session() as local_session:
                merged = local_session.merge(entidade)
                local_session.commit()
                return merged
        merged = session.merge(entidade)
        session.flush()
        return merged

    def remover(self, id: int, session: Session | None = None) -> bool:
        if session is None:
            with self._get_session() as local_session:
                obj = local_session.query(self.modelo_classe).filter_by(id=id).first()
                if obj:
                    local_session.delete(obj)
                    local_session.commit()
                    return True
                return False
        obj = session.query(self.modelo_classe).filter_by(id=id).first()
        if obj:
            session.delete(obj)
            session.flush()
            return True
        return False