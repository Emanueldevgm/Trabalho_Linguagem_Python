import sys
from PySide6.QtWidgets import QApplication
from src.utils.database import criar_tabelas, obter_session
from src.models.usuario import Usuario
from src.repositories.usuario_repo import UsuarioRepositorio
from src.gui.login_window import LoginWindow
from src.gui.main_window import MainWindow

def criar_usuario_admin():
    repo = UsuarioRepositorio()
    admin = repo.obter_por_username("admin")
    if not admin:
        admin = Usuario(username="admin", perfil="admin")
        admin.definir_senha("admin123")
        repo.adicionar(admin)
        print("Usuário admin criado: admin / admin123")

def main():
    criar_tabelas()
    criar_usuario_admin()
    app = QApplication(sys.argv)
    login = LoginWindow()
    if login.exec():
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec())
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()