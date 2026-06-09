                                  
from src.models.usuario import Usuario
from src.repositories.repositorio_base import RepositorioBase

class UsuarioRepositorio(RepositorioBase[Usuario]):
    def __init__(self):
        super().__init__(Usuario)

    def obter_por_username(self, username: str) -> Usuario | None:
        with self._get_session() as session:
            return session.query(Usuario).filter_by(username=username).first()