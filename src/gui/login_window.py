from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QLabel, QMessageBox, QCheckBox,
    QFrame, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from src.repositories.usuario_repo import UsuarioRepositorio
from src.gui.styles import COLORS, TYPOGRAPHY, BORDERS

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.usuario_repo = UsuarioRepositorio()
        self.setWindowTitle("Inventário IA")
        self.setFixedSize(440, 560)
        self.setModal(True)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        container = QFrame()
        container.setObjectName("loginContainer")
        container.setStyleSheet(f"""
            QFrame#loginContainer {{
                background-color: {COLORS['white']};
                border-radius: {BORDERS['radius_xl']};
                border: 1px solid {COLORS['gray_100']};
            }}
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 4)
        container.setGraphicsEffect(shadow)
        
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(40, 48, 40, 40)
        container_layout.setSpacing(0)
        
        icon_label = QLabel("\U0001F4E6")
        icon_label.setAlignment(Qt.AlignCenter) # type: ignore
        icon_label.setStyleSheet("""
            font-size: 48px;
            padding: 0px;
            margin: 0px;
        """)
        container_layout.addWidget(icon_label)
        container_layout.addSpacing(16)
        
        title = QLabel("Inventário IA")
        title.setAlignment(Qt.AlignCenter) # type: ignore
        title.setStyleSheet(f"""
            font-size: {TYPOGRAPHY['font_size_2xl']};
            font-weight: {TYPOGRAPHY['font_weight_bold']};
            color: {COLORS['dark']};
            padding: 0px;
            margin: 0px;
        """)
        container_layout.addWidget(title)
        
        subtitle = QLabel("Sistema Inteligente de Gestão")
        subtitle.setAlignment(Qt.AlignCenter) # type: ignore
        subtitle.setStyleSheet(f"""
            font-size: {TYPOGRAPHY['font_size_sm']};
            color: {COLORS['gray_500']};
            padding: 0px;
        """)
        container_layout.addWidget(subtitle)
        container_layout.addSpacing(32)
        
        form_card = QFrame()
        form_card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['gray_50']};
                border-radius: {BORDERS['radius_lg']};
                border: 1px solid {COLORS['gray_100']};
            }}
        """)
        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(24, 24, 24, 24)
        form_layout.setSpacing(16)
        
        user_label = QLabel("Utilizador")
        user_label.setStyleSheet(f"""
            font-size: {TYPOGRAPHY['font_size_sm']};
            font-weight: {TYPOGRAPHY['font_weight_semibold']};
            color: {COLORS['gray_700']};
            text-transform: uppercase;
            letter-spacing: 0.5px;
        """)
        form_layout.addWidget(user_label)
        
        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("Digite seu nome de utilizador")
        self.input_usuario.setFixedHeight(46)
        form_layout.addWidget(self.input_usuario)
        
        pass_label = QLabel("Palavra-passe")
        pass_label.setStyleSheet(f"""
            font-size: {TYPOGRAPHY['font_size_sm']};
            font-weight: {TYPOGRAPHY['font_weight_semibold']};
            color: {COLORS['gray_700']};
            text-transform: uppercase;
            letter-spacing: 0.5px;
        """)
        form_layout.addWidget(pass_label)
        
        pass_container = QHBoxLayout()
        pass_container.setSpacing(0)
        
        self.input_senha = QLineEdit()
        self.input_senha.setEchoMode(QLineEdit.Password) # type: ignore
        self.input_senha.setPlaceholderText("Digite sua palavra-passe")
        self.input_senha.setFixedHeight(46)
        
        self.toggle_pass_btn = QPushButton("\U0001F441")
        self.toggle_pass_btn.setFixedSize(46, 46)
        self.toggle_pass_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                color: {COLORS['gray_500']};
                font-size: 18px;
                padding: 0px;
            }}
            QPushButton:hover {{
                color: {COLORS['gray_700']};
            }}
        """)
        self.toggle_pass_btn.clicked.connect(self.toggle_password_visibility)
        
        pass_container.addWidget(self.input_senha)
        pass_container.addWidget(self.toggle_pass_btn)
        form_layout.addLayout(pass_container)
        
        options_layout = QHBoxLayout()
        self.chk_lembrar = QCheckBox("Manter sessão iniciada")
        options_layout.addWidget(self.chk_lembrar)
        form_layout.addLayout(options_layout)
        
        container_layout.addWidget(form_card)
        container_layout.addSpacing(24)
        
        self.btn_login = QPushButton("Iniciar Sessão")
        self.btn_login.setFixedHeight(48)
        self.btn_login.setMinimumHeight(48)
        self.btn_login.setCursor(Qt.PointingHandCursor) # type: ignore
        self.btn_login.clicked.connect(self.autenticar)
        self.btn_login.setDefault(True)
        self.btn_login.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['primary']};
                color: white;
                border: none;
                border-radius: {BORDERS['radius_md']};
                padding: 10px 20px;
                font-weight: {TYPOGRAPHY['font_weight_semibold']};
                font-size: {TYPOGRAPHY['font_size_base']};
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary_dark']};
            }}
            QPushButton:pressed {{
                background-color: #1e40af;
            }}
            QPushButton:disabled {{
                background-color: {COLORS['gray_300']};
                color: {COLORS['gray_500']};
            }}
        """)
        container_layout.addWidget(self.btn_login)
        
        container_layout.addSpacing(16)
        
        footer = QLabel("© 2026 Inventário IA • v1.0.0")
        footer.setAlignment(Qt.AlignCenter) # type: ignore
        footer.setStyleSheet(f"""
            font-size: {TYPOGRAPHY['font_size_sm']};
            color: {COLORS['gray_500']};
        """)
        container_layout.addWidget(footer)
        
        main_layout.addWidget(container)
        
        self.input_usuario.setFocus()

    def toggle_password_visibility(self):
        if self.input_senha.echoMode() == QLineEdit.Password: # type: ignore
            self.input_senha.setEchoMode(QLineEdit.Normal) # type: ignore
            self.toggle_pass_btn.setText("\U0001F441\U0000200D\U0001F5E8")
        else:
            self.input_senha.setEchoMode(QLineEdit.Password) # type: ignore
            self.toggle_pass_btn.setText("\U0001F441")

    def autenticar(self):
        username = self.input_usuario.text().strip()
        senha = self.input_senha.text()
        
        if not username or not senha:
            QMessageBox.warning(
                self, 
                "Campos obrigatórios",
                "Por favor, preencha o nome de utilizador e a palavra-passe."
            )
            return

        self.btn_login.setEnabled(False)
        self.btn_login.setText("Autenticando...")
        self.btn_login.repaint()

        try:
            usuario = self.usuario_repo.obter_por_username(username)
            if usuario and usuario.verificar_senha(senha):
                self.accept()
            else:
                QMessageBox.critical(
                    self,
                    "Falha na autenticação",
                    "Nome de utilizador ou palavra-passe inválidos."
                )
                self.btn_login.setEnabled(True)
                self.btn_login.setText("Iniciar Sessão")
                self.input_senha.clear()
                self.input_senha.setFocus()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erro de autenticação",
                f"Ocorreu um erro ao autenticar:\n{str(e)}"
            )
            self.btn_login.setEnabled(True)
            self.btn_login.setText("Iniciar Sessão")