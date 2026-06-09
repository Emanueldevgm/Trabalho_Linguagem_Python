                        
"""
Script para gerar dados de vendas históricas fictícias para testar o módulo de IA.
Execute apenas após cadastrar pelo menos um produto.
"""
import random
from datetime import datetime, timedelta
from src.utils.database import obter_session
from src.models.produto import Produto
from src.models.venda import Venda
from src.repositories.produto_repo import ProdutoRepositorio

def gerar_vendas_teste(produto_id: int, dias: int = 60):
    """Gera vendas aleatórias para os últimos `dias` dias."""
    with obter_session() as session:
        produto = session.query(Produto).filter_by(id=produto_id).first()
        if not produto:
            print(f"Produto com ID {produto_id} não encontrado.")
            return

        data_fim = datetime.now()
        data_inicio = data_fim - timedelta(days=dias)
        vendas = []
        data_atual = data_inicio
        while data_atual <= data_fim:
                                                                    
            qtd = random.randint(5, 30)
            if data_atual.weekday() >= 5:                              
                qtd = random.randint(2, 15)
            valor_total = qtd * produto.preco_unitario
            venda = Venda(
                produto_id=produto_id,
                quantidade=qtd,
                valor_total=valor_total,
                data=data_atual
            )
            vendas.append(venda)
            data_atual += timedelta(days=1)

        session.add_all(vendas)
        session.commit()
        print(f"{len(vendas)} vendas geradas para o produto '{produto.nome}'.")

if __name__ == "__main__":
                                  
    repo = ProdutoRepositorio()
    produtos = repo.listar()
    if not produtos:
        print("Nenhum produto cadastrado. Cadastre um produto primeiro via interface.")
    else:
        print("Produtos disponíveis:")
        for p in produtos:
            print(f"ID: {p.id} - Nome: {p.nome}")
        try:
            pid = int(input("Digite o ID do produto para gerar vendas de teste: "))
            gerar_vendas_teste(pid, dias=60)
        except ValueError:
            print("ID inválido.")