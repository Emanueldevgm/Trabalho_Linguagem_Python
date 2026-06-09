                        
"""
Script para gerar dados de teste para o sistema de inventário.
Gera vendas, compras e usuários fictícios para testar a IA e o dashboard.
Execute apenas após cadastrar pelo menos um produto.
"""
import random
from datetime import datetime, timedelta
from src.utils.database import obter_session
from src.models.produto import Produto
from src.models.venda import Venda
from src.models.compra import Compra
from src.models.usuario import Usuario
from src.repositories.produto_repo import ProdutoRepositorio


def gerar_vendas_teste(produto_id: int, dias: int = 60, vendas_por_dia: tuple = (5, 30)):
    """
    Gera vendas aleatórias para os últimos `dias` dias.
    
    Args:
        produto_id: ID do produto
        dias: Número de dias de histórico a gerar
        vendas_por_dia: Tupla (mín, máx) de quantidade por dia
    """
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
            # Menor quantidade nos fins de semana (quinta a domingo)
            if data_atual.weekday() >= 4:
                qtd = random.randint(2, 15)
            else:
                # Dias úteis: mais vendas
                qtd = random.randint(vendas_por_dia[0], vendas_por_dia[1])
            
            # Adiciona variação aleatória (20% de chance de pico de demanda)
            if random.random() < 0.2:
                qtd = int(qtd * random.uniform(1.5, 2.5))
            
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
        print(f"✓ {len(vendas)} vendas geradas para '{produto.nome}' ({dias} dias)")


def gerar_compras_teste(produto_id: int, dias: int = 60):
    """
    Gera dados de compra históricos para um produto.
    
    Args:
        produto_id: ID do produto
        dias: Número de dias de histórico a gerar
    """
    with obter_session() as session:
        produto = session.query(Produto).filter_by(id=produto_id).first()
        if not produto:
            print(f"Produto com ID {produto_id} não encontrado.")
            return

        data_fim = datetime.now()
        data_inicio = data_fim - timedelta(days=dias)
        compras = []
        
        # Gera uma compra a cada 7-14 dias em média
        data_atual = data_inicio
        while data_atual <= data_fim:
            # Decide se faz compra neste dia (probabilidade)
            if random.random() < 0.15:  # 15% de chance por dia
                quantidade = random.randint(50, 200)
                # Custo é ~60% do preço de venda (margem típica)
                custo_unitario = produto.preco_unitario * random.uniform(0.4, 0.6)
                custo_total = quantidade * custo_unitario
                
                compra = Compra(
                    produto_id=produto_id,
                    quantidade=quantidade,
                    custo_total=custo_total,
                    data=data_atual
                )
                compras.append(compra)
            
            data_atual += timedelta(days=1)

        if compras:
            session.add_all(compras)
            session.commit()
            print(f"✓ {len(compras)} compras geradas para '{produto.nome}'")
        else:
            print(f"⚠ Nenhuma compra gerada para '{produto.nome}' (tente aumentar os dias)")


def gerar_usuarios_teste():
    """Gera usuários de teste com diferentes perfis."""
    with obter_session() as session:
        usuarios_teste = [
            ("admin", "admin123", "admin"),
            ("vendedor1", "senha123", "vendedor"),
            ("vendedor2", "senha123", "vendedor"),
            ("gerente", "senha123", "gerente"),
            ("operador", "senha123", "operador"),
        ]
        
        usuarios_criados = []
        for username, senha, perfil in usuarios_teste:
            # Verifica se o usuário já existe
            if session.query(Usuario).filter_by(username=username).first():
                print(f"⚠ Usuário '{username}' já existe")
                continue
            
            usuario = Usuario(username=username, perfil=perfil)
            usuario.definir_senha(senha)
            session.add(usuario)
            usuarios_criados.append(username)
        
        if usuarios_criados:
            session.commit()
            print(f"✓ {len(usuarios_criados)} usuários de teste criados: {', '.join(usuarios_criados)}")
        else:
            print("⚠ Todos os usuários já existem")


def limpar_dados_teste(produto_id: int = None): # type: ignore
    """
    Remove dados de teste (vendas e compras) do banco.
    
    Args:
        produto_id: Se fornecido, limpa apenas este produto. Se None, pergunta ao usuário.
    """
    with obter_session() as session:
        if produto_id is None:
            print("\n⚠ Esta ação removerá TODAS as vendas e compras!")
            confirm = input("Deseja continuar? (s/n): ").lower()
            if confirm != 's':
                print("Cancelado.")
                return
            
            vendas_removidas = session.query(Venda).delete()
            compras_removidas = session.query(Compra).delete()
        else:
            produto = session.query(Produto).filter_by(id=produto_id).first()
            if not produto:
                print(f"Produto com ID {produto_id} não encontrado.")
                return
            
            vendas_removidas = session.query(Venda).filter_by(produto_id=produto_id).delete()
            compras_removidas = session.query(Compra).filter_by(produto_id=produto_id).delete()
            print(f"Limpando dados do produto: {produto.nome}")
        
        session.commit()
        print(f"✓ {vendas_removidas} vendas removidas")
        print(f"✓ {compras_removidas} compras removidas")


def menu_principal():
    """Menu interativo para gerar dados de teste."""
    repo = ProdutoRepositorio()
    produtos = repo.listar()
    
    if not produtos:
        print("❌ Nenhum produto cadastrado. Cadastre um produto primeiro via interface.")
        return
    
    print("\n" + "="*60)
    print("  GERADOR DE DADOS DE TESTE - SISTEMA DE INVENTÁRIO")
    print("="*60)
    
    while True:
        print("\n📋 Produtos disponíveis:")
        for p in produtos:
            print(f"   ID: {p.id:2d} | {p.nome:20s} | R$ {p.preco_unitario:.2f}")
        
        print("\n🔧 Menu:")
        print("  1 - Gerar vendas para um produto")
        print("  2 - Gerar compras para um produto")
        print("  3 - Gerar dados para TODOS os produtos")
        print("  4 - Gerar usuários de teste")
        print("  5 - Limpar dados de teste")
        print("  6 - Sair")
        
        opcao = input("\nEscolha uma opção (1-6): ").strip()
        
        if opcao == '1':
            try:
                pid = int(input("Digite o ID do produto: "))
                dias = input("Número de dias (padrão 60): ").strip() or "60"
                gerar_vendas_teste(pid, int(dias))
            except ValueError:
                print("❌ Entrada inválida.")
        
        elif opcao == '2':
            try:
                pid = int(input("Digite o ID do produto: "))
                dias = input("Número de dias (padrão 60): ").strip() or "60"
                gerar_compras_teste(pid, int(dias))
            except ValueError:
                print("❌ Entrada inválida.")
        
        elif opcao == '3':
            dias = input("Número de dias (padrão 60): ").strip() or "60"
            dias = int(dias)
            for produto in produtos:
                print(f"\n⏳ Processando {produto.nome}...")
                gerar_vendas_teste(produto.id, dias) # type: ignore
                gerar_compras_teste(produto.id, dias) # type: ignore
            print("\n✓ Dados gerados para todos os produtos!")
        
        elif opcao == '4':
            gerar_usuarios_teste()
        
        elif opcao == '5':
            try:
                pid_input = input("ID do produto a limpar (deixe em branco para limpar tudo): ").strip()
                pid = int(pid_input) if pid_input else None
                limpar_dados_teste(pid) # type: ignore
            except ValueError:
                print("❌ Entrada inválida.")
        
        elif opcao == '6':
            print("\n👋 Até logo!")
            break
        
        else:
            print("❌ Opção inválida.")


if __name__ == "__main__":
    menu_principal()