# src/models/contratos.py
from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic
import pandas as pd

T = TypeVar('T')

class Repositorio(ABC, Generic[T]):
    """Contrato para repositórios genéricos."""
    @abstractmethod
    def adicionar(self, entidade: T) -> T:
        pass

    @abstractmethod
    def obter_por_id(self, id: int) -> T | None:
        pass

    @abstractmethod
    def listar(self) -> List[T]:
        pass

    @abstractmethod
    def atualizar(self, entidade: T) -> T:
        pass

    @abstractmethod
    def remover(self, id: int) -> bool:
        pass

class ModeloIA(ABC):
    """Contrato para modelos de Inteligência Artificial."""
    @abstractmethod
    def treinar(self, dados_historicos: pd.DataFrame) -> None:
        """Recebe dados com colunas: data, quantidade."""
        pass

    @abstractmethod
    def prever(self, passos_futuros: int) -> pd.DataFrame:
        """Retorna DataFrame com colunas: data_previsao, quantidade_prevista."""
        pass

    @abstractmethod
    def salvar_modelo(self, caminho: str) -> None:
        pass

    @abstractmethod
    def carregar_modelo(self, caminho: str) -> None:
        pass