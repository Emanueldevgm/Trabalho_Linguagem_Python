                                          
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
    def calcular_media_vendas_diarias(self, produto_id: int, dias: int = 30) -> float:
        """Calcula a média diária de vendas para um produto num período."""
        historico = self.venda_repo.obter_historico_por_produto(produto_id, dias=dias)
        if historico.empty:
            return 0.0
        total_vendido = float(historico['quantidade'].sum())
        return round(total_vendido / dias, 2)

    @log_execucao
    def calcular_ponto_pedido(self, produto_id: int, dias: int = 30) -> int:
        """Aplica a fórmula de ponto de pedido a partir da demanda média e lead time."""
        produto = self.produto_repo.obter_por_id(produto_id)
        if not produto:
            raise ProdutoNaoEncontradoError(produto_id)
        media_diaria = self.calcular_media_vendas_diarias(produto_id, dias)
        ponto_pedido = media_diaria * produto.lead_time_dias + produto.estoque_minimo
        return int(round(ponto_pedido))

    @log_execucao
    def calcular_dias_estoque(self, produto_id: int, dias: int = 30) -> float:
        """Calcula quantos dias o estoque atual suporta com base nas vendas médias."""
        produto = self.produto_repo.obter_por_id(produto_id)
        if not produto:
            raise ProdutoNaoEncontradoError(produto_id)
        media_diaria = self.calcular_media_vendas_diarias(produto_id, dias)
        if media_diaria <= 0:
            return float('inf')
        return round(produto.estoque_atual / media_diaria, 1)

    @log_execucao
    def obter_metricas_inventario(self, produto_id: int, dias: int = 30) -> dict:
        """Obtém métricas de estoque para análise: média, ponto de pedido e recomendação."""
        produto = self.produto_repo.obter_por_id(produto_id)
        if not produto:
            raise ProdutoNaoEncontradoError(produto_id)
        media_diaria = self.calcular_media_vendas_diarias(produto_id, dias)
        ponto_pedido = self.calcular_ponto_pedido(produto_id, dias)
        dias_estoque = self.calcular_dias_estoque(produto_id, dias)
        quantidade_recomendada = max(0, ponto_pedido - produto.estoque_atual)

        return {
            'produto_id': produto_id,
            'media_diaria': media_diaria,
            'dias_estoque': dias_estoque,
            'ponto_pedido': ponto_pedido,
            'estoque_atual': produto.estoque_atual,
            'quantidade_recomendada': quantidade_recomendada
        }

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
        if produto.estoque_atual < quantidade:                                           
            raise EstoqueInsuficienteError(produto.nome, produto.estoque_atual, quantidade)                                      

                          
        produto.estoque_atual -= quantidade                                              
        self.produto_repo.atualizar(produto, session=session)

                                
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

                          
        produto.estoque_atual += quantidade                                              
        self.produto_repo.atualizar(produto, session=session)

                                 
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
            ponto_pedido = ponto_pedido_dict.get(produto.id, 0)                                                       
            if produto.estoque_atual <= ponto_pedido:
                alerta.append(produto)
        return alerta

    def recomendar_compra(self, incremento_pedido: int = 5) -> List[dict]:
        """Retorna recomendações de compra para produtos perto ou abaixo do ponto de pedido."""
        produtos = self.produto_repo.listar()
        recomendacoes = []
        for produto in produtos:
            media_diaria = self.calcular_media_vendas_diarias(produto.id)
            ponto_pedido = int(round(media_diaria * produto.lead_time_dias + produto.estoque_minimo))
            if produto.estoque_atual <= ponto_pedido:
                quantidade_recomendada = max(0, ponto_pedido - produto.estoque_atual)
                recomendacoes.append({
                    'produto': produto,
                    'media_diaria': media_diaria,
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