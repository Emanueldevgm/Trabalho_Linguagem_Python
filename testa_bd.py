# testa_bd.py
import sys
import os
sys.path.insert(0, os.getcwd())

from src.utils.database import criar_tabelas, obter_session
from src.models.usuario import Usuario
from src.models.produto import Produto
from src.models.venda import Venda
from src.models.compra import Compra
from src.models.previsao import Previsao

print("Criando tabelas...")
criar_tabelas()
print("Tabelas criadas com sucesso!")

# Testa inserção de um usuário admin
session = obter_session()
admin = session.query(Usuario).filter_by(username="admin").first()
if not admin:
    admin = Usuario(username="admin", perfil="admin")
    admin.definir_senha("admin123")
    session.add(admin)
    session.commit()
    print("Usuário admin criado com sucesso (admin/admin123).")
else:
    print("Usuário admin já existe.")

# Lista produtos
produtos = session.query(Produto).all()
print(f"Total de produtos no banco: {len(produtos)}")

session.close()
print("Banco de dados OK! Arquivo: data/inventario.db")