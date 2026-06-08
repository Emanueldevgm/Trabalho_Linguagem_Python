# src/repositories/produto_repo.py
from src.models.produto import Produto
from src.repositories.repositorio_base import RepositorioBase

class ProdutoRepositorio(RepositorioBase[Produto]):
    def __init__(self):
        super().__init__(Produto)