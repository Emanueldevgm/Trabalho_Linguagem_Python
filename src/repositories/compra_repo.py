# src/repositories/compra_repo.py
from src.models.compra import Compra
from src.repositories.repositorio_base import RepositorioBase

class CompraRepositorio(RepositorioBase[Compra]):
    def __init__(self):
        super().__init__(Compra)