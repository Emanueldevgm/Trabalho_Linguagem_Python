                       
"""Exceções customizadas do sistema."""

class InventarioException(Exception):
    """Exceção base do sistema."""
    pass

class EstoqueInsuficienteError(InventarioException):
    def __init__(self, produto_nome: str, estoque_atual: int, solicitado: int):
        self.produto_nome = produto_nome
        self.estoque_atual = estoque_atual
        self.solicitado = solicitado
        super().__init__(
            f"Estoque insuficiente para '{produto_nome}': "
            f"tem {estoque_atual}, solicitado {solicitado}"
        )

class ProdutoNaoEncontradoError(InventarioException):
    def __init__(self, produto_id: int):
        super().__init__(f"Produto com ID {produto_id} não encontrado.")

class ModeloNaoTreinadoError(InventarioException):
    def __init__(self, produto_id: int = None):                                      
        msg = "Modelo de IA não treinado."
        if produto_id:
            msg = f"Modelo de IA para produto {produto_id} não treinado."
        super().__init__(msg)

class DadosInsuficientesError(InventarioException):
    def __init__(self, produto_id: int, minimo: int, atual: int):
        super().__init__(
            f"Produto {produto_id}: precisa de {minimo} registros, tem {atual}."
        )

class FalhaAutenticacaoError(InventarioException):
    pass

class TransacaoError(InventarioException):
    pass