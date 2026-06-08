# src/utils/decoradores.py
"""Decoradores personalizados para logging, transações e validações."""
import functools
import logging
from src.utils.context_managers import Temporizador
from src.utils.excecoes import EstoqueInsuficienteError, TransacaoError, ProdutoNaoEncontradoError

# Configuração básica de log
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='logs/sistema.log',
    filemode='a'
)

def log_execucao(func):
    """Decorador que registra chamada de métodos com argumentos."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        args_repr = repr(args[1:]) if len(args) > 1 else ""
        logger.info(f"Chamando {func.__name__} com args={args_repr} kwargs={kwargs}")
        with Temporizador(func.__name__):
            try:
                resultado = func(*args, **kwargs)
                try:
                    logger.info(f"{func.__name__} retornou {resultado}")
                except Exception:
                    logger.info(f"{func.__name__} retornou um resultado do tipo {type(resultado).__name__}")
                return resultado
            except Exception as e:
                logger.error(f"Erro em {func.__name__}: {str(e)}")
                raise
    return wrapper

def transacional(session_maker):
    """Decorador que gerencia transação do banco."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            session = session_maker()
            try:
                resultado = func(*args, **kwargs, session=session)
                session.commit()
                return resultado
            except Exception as e:
                session.rollback()
                raise TransacaoError(f"Falha na transação: {str(e)}")
            finally:
                session.close()
        return wrapper
    return decorator

def validar_estoque(controller_method):
    """Decorador que verifica estoque antes de registrar venda (usado em métodos do controller)."""
    @functools.wraps(controller_method)
    def wrapper(self, produto_id, quantidade, *args, **kwargs):
        # O controller deve ter um atributo _produto_repo (ou similar)
        produto = self.produto_repo.obter_por_id(produto_id)  # ajuste conforme seu controller
        if not produto:
            raise ProdutoNaoEncontradoError(produto_id)
        if produto.estoque_atual < quantidade:
            raise EstoqueInsuficienteError(produto.nome, produto.estoque_atual, quantidade)
        return controller_method(self, produto_id, quantidade, *args, **kwargs)
    return wrapper