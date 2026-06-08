# src/controllers/inventario_controller.py
"""
Controlador responsável pela lógica de negócio do inventário:
produtos, vendas, compras e alertas de estoque.
"""
from typing import List, Dict
from src.models.produto import Produto
from src.models.venda import Venda
from src.models.compra import Compra
from src.repositories.produto_repo import ProdutoRepositorio
from src.repositories.venda_repo import VendaRepositorio
from src.repositories.compra_repo import CompraRepositorio
from src.utils.database import obter_session
from src.utils.decoradores import log_execucao, transacional
from src.utils.excecoes import ProdutoNaoEncontradoError, EstoqueInsuficienteError


class InventarioController:
    """Gerencia o fluxo de produtos, vendas, compras e alertas."""

    def __init__(self):
        self.produto_repo = ProdutoRepositorio()
        self.venda_repo = VendaRepositorio()
        self.compra_repo = CompraRepositorio()

    @log_execucao
    @transacional(obter_session)
    def cadastrar_produto(
        self,
        nome: str,
        categoria: str,
        preco: float,
        estoque_inicial: int = 0,
        session=None
    ) -> Produto:
        """Cadastra um novo produto no sistema."""
        produto = Produto(
            nome=nome,
            categoria=categoria,
            preco_unitario=preco,
            estoque_atual=estoque_inicial
        )
        return self.produto_repo.adicionar(produto, session=session)

    @log_execucao
    def listar_produtos(self) -> List[Produto]:
        """Retorna todos os produtos cadastrados."""
        return self.produto_repo.listar()

    @log_execucao
    @transacional(obter_session)
    def atualizar_produto(self, produto_id: int, session=None, **dados) -> Produto:
        """Atualiza os dados de um produto existente."""
        produto = self.produto_repo.obter_por_id(produto_id, session=session)
        if not produto:
            raise ProdutoNaoEncontradoError(produto_id)
        for key, value in dados.items():
            if hasattr(produto, key):
                setattr(produto, key, value)
        return self.produto_repo.atualizar(produto, session=session)

    @log_execucao
    @transacional(obter_session)
    def registrar_venda(self, produto_id: int, quantidade: int, valor_total: float, session=None) -> Venda:
        """Registra uma venda, atualizando o estoque e criando o registro."""
        produto = self.produto_repo.obter_por_id(produto_id, session=session)
        if not produto:
            raise ProdutoNaoEncontradoError(produto_id)
        if produto.estoque_atual < quantidade: # pyright: ignore[reportGeneralTypeIssues]
            raise EstoqueInsuficienteError(produto.nome, produto.estoque_atual, quantidade) # pyright: ignore[reportArgumentType]

        # Atualiza estoque
        produto.estoque_atual -= quantidade # pyright: ignore[reportAttributeAccessIssue]
        self.produto_repo.atualizar(produto, session=session)

        # Cria registro de venda
        venda = Venda(
            produto_id=produto_id,
            quantidade=quantidade,
            valor_total=valor_total
        )
        return self.venda_repo.adicionar(venda, session=session)

    @log_execucao
    @transacional(obter_session)
    def registrar_compra(self, produto_id: int, quantidade: int, custo_total: float, session=None) -> Compra:
        """Registra uma compra (reposição), atualizando o estoque."""
        produto = self.produto_repo.obter_por_id(produto_id, session=session)
        if not produto:
            raise ProdutoNaoEncontradoError(produto_id)

        # Atualiza estoque
        produto.estoque_atual += quantidade # pyright: ignore[reportUnknownAttributeType]
        self.produto_repo.atualizar(produto, session=session)

        # Cria registro de compra
        compra = Compra(
            produto_id=produto_id,
            quantidade=quantidade,
            custo_total=custo_total
        )
        return self.compra_repo.adicionar(compra, session=session)

    def obter_estoque_baixo(self, ponto_pedido_dict: Dict[int, int]) -> List[Produto]:
        """
        Retorna produtos cujo estoque atual está abaixo do ponto de pedido.
        O dicionário deve conter {produto_id: ponto_pedido}.
        """
        produtos = self.produto_repo.listar()
        alerta = []
        for produto in produtos:
            ponto_pedido = ponto_pedido_dict.get(produto.id, 0) # pyright: ignore[reportArgumentType, reportCallIssue]
            if produto.estoque_atual <= ponto_pedido:
                alerta.append(produto)
        return alerta

    def recomendar_compra(self, incremento_pedido: int = 5) -> List[dict]:
        """Retorna recomendações de compra para produtos perto ou abaixo do ponto de pedido."""
        produtos = self.produto_repo.listar()
        recomendacoes = []
        for produto in produtos:
            ponto_pedido = produto.estoque_minimo + incremento_pedido
            if produto.estoque_atual <= ponto_pedido:
                quantidade_recomendada = max(0, ponto_pedido + produto.lead_time_dias - produto.estoque_atual)
                recomendacoes.append({
                    'produto': produto,
                    'estoque_atual': produto.estoque_atual,
                    'ponto_pedido': ponto_pedido,
                    'quantidade_recomendada': quantidade_recomendada
                })
        return recomendacoes

    @log_execucao
    @transacional(obter_session)
    def remover_produto(self, produto_id: int, session=None) -> bool:
        """Remove um produto pelo ID. Retorna True se removido, lança erro se não existir."""
        produto = self.produto_repo.obter_por_id(produto_id, session=session)
        if not produto:
            raise ProdutoNaoEncontradoError(produto_id)
        return self.produto_repo.remover(produto_id, session=session)