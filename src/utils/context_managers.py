# src/utils/context_managers.py
"""Context managers personalizados."""
import time
import logging
from typing import Optional, Type
from types import TracebackType
from sqlalchemy.orm import sessionmaker # pyright: ignore[reportUnusedImport]

class ConexaoBanco:
    """Gerencia sessão do banco com commit/rollback automático."""
    def __init__(self, session_factory): # pyright: ignore[reportMissingParameterType, reportUnknownParameterType]
        self.session_factory = session_factory
        self.session = None

    def __enter__(self): # pyright: ignore[reportUnknownParameterType]
        self.session = self.session_factory() # pyright: ignore[reportUnknownMemberType]
        return self.session # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if exc_type:
            self.session.rollback() # pyright: ignore[reportOptionalMemberAccess, reportUnknownMemberType]
        else:
            self.session.commit() # pyright: ignore[reportOptionalMemberAccess, reportUnknownMemberType]
        self.session.close() # pyright: ignore[reportOptionalMemberAccess, reportUnknownMemberType]

class Temporizador:
    """Mede tempo de execução de um bloco."""
    def __init__(self, nome_tarefa: str = "Bloco"):
        self.nome_tarefa = nome_tarefa
        self.logger = logging.getLogger(__name__)

    def __enter__(self):
        self.inicio = time.time()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        duracao = time.time() - self.inicio
        self.logger.info(f"{self.nome_tarefa} executado em {duracao:.4f} segundos")