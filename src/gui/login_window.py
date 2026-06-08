# src/gui/login_window.py
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit,
    QPushButton, QLabel, QMessageBox, QHBoxLayout,
    QCheckBox, QSizePolicy
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QIcon
from src.repositories.usuario_repo import UsuarioRepositorio


class LoginWindow(QDialog):
    """Janela de login com design melhorado, logo opcional,
    checkbox 'Lembrar-me' e opção 'Mostrar senha'."""

    def __init__(self):
        super().__init__()
        self.usuario_repo = UsuarioRepositorio()
        self.setWindowTitle("Login - Inventário IA")
        self.setFixedSize(420, 300)
        self.setModal(True)
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet(self._estilos())

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # Logo (opcional)
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignCenter)
        try:
            pix = QPixmap("assets/logo.png")
            if not pix.isNull():
                pix = pix.scaledToWidth(160, Qt.SmoothTransformation)
                logo_label.setPixmap(pix)
        except Exception:
            pass

        # Campos com ícones opcionais
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)

        # Usuário (ícone + input)
        usuario_layout = QHBoxLayout()
        usuario_layout.setSpacing(8)
        user_icon = QLabel()
        try:
            upix = QPixmap("assets/icons/user.png")
            if not upix.isNull():
                upix = upix.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                user_icon.setPixmap(upix)
        except Exception:
            pass
        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("Nome de utilizador")
        self.input_usuario.setFixedHeight(36)
        usuario_layout.addWidget(user_icon)
        usuario_layout.addWidget(self.input_usuario)

        # Senha (ícone + input + mostrar)
        senha_layout = QHBoxLayout()
        senha_layout.setSpacing(8)
        lock_icon = QLabel()
        try:
            lpix = QPixmap("assets/icons/lock.png")
            if not lpix.isNull():
                lpix = lpix.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                lock_icon.setPixmap(lpix)
        except Exception:
            pass
        self.input_senha = QLineEdit()
        self.input_senha.setEchoMode(QLineEdit.Password)
        self.input_senha.setPlaceholderText("Palavra-passe")
        self.input_senha.setFixedHeight(36)

        self.chk_mostrar = QCheckBox("Mostrar senha")
        self.chk_mostrar.stateChanged.connect(self._alternar_senha)
        self.chk_mostrar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        senha_layout.addWidget(lock_icon)
        senha_layout.addWidget(self.input_senha)
        senha_layout.addWidget(self.chk_mostrar)

        # Opções adicionais
        options_layout = QHBoxLayout()
        self.chk_lembrar = QCheckBox("Lembrar-me")
        options_layout.addWidget(self.chk_lembrar)
        options_layout.addStretch()

        # Botões
        btn_layout = QHBoxLayout()
        self.btn_login = QPushButton("Entrar")
        try:
            ik = QIcon("assets/icons/login.png")
            if not ik.isNull():
                self.btn_login.setIcon(ik)
                self.btn_login.setIconSize(QSize(16, 16))
        except Exception:
            pass
        self.btn_login.clicked.connect(self.autenticar)
        self.btn_login.setDefault(True)

        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.setObjectName("cancel")
        try:
            ck = QIcon("assets/icons/cancel.png")
            if not ck.isNull():
                self.btn_cancel.setIcon(ck)
                self.btn_cancel.setIconSize(QSize(16, 16))
        except Exception:
            pass
        self.btn_cancel.clicked.connect(self.reject)

        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_login)

        # Montagem final
        main_layout.addWidget(logo_label)
        form_layout.addWidget(QLabel("Usuário"))
        form_layout.addLayout(usuario_layout)
        form_layout.addWidget(QLabel("Senha"))
        form_layout.addLayout(senha_layout)
        form_layout.addLayout(options_layout)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

    def _alternar_senha(self, state):
        if state == Qt.Checked:
            self.input_senha.setEchoMode(QLineEdit.Normal)
        else:
            self.input_senha.setEchoMode(QLineEdit.Password)

    def autenticar(self):
        username = self.input_usuario.text().strip()
        senha = self.input_senha.text()
        if not username or not senha:
            QMessageBox.warning(self, "Erro", "Preencha o nome de utilizador e a palavra-passe.")
            return

        usuario = self.usuario_repo.obter_por_username(username)
        if usuario and usuario.verificar_senha(senha):
            # Aqui poderíamos guardar a preferência 'lembrar-me' se implementado
            self.accept()
        else:
            QMessageBox.critical(self, "Falha", "Nome de utilizador ou palavra-passe inválidos.")

    def _estilos(self) -> str:
        return """
        QDialog { background-color: #ffffff; color: #000000; }
        QLabel { font-size: 12px; color: #000000; }
        QLineEdit { background: white; border: 1px solid #cfd8dc; border-radius: 6px; padding-left: 8px; color: #000000; }
        QLineEdit::placeholder { color: #9e9e9e; }
        QPushButton { background-color: #1976d2; color: white; padding: 8px 14px; border-radius: 6px; }
        QPushButton#cancel { background-color: #9e9e9e; color: white; }
        QPushButton:hover { background-color: #1565c0; }
        QCheckBox { padding: 4px; color: #000000; }
        QLabel { color: #000000; }
        QVBoxLayout { margin: 12px; }
        """