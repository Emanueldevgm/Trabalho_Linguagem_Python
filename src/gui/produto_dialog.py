from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QLineEdit, QDoubleSpinBox, QSpinBox,
    QPushButton, QLabel, QMessageBox, QFrame,
    QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from src.gui.styles import COLORS, TYPOGRAPHY, BORDERS
from src.utils.constants import CURRENCY_SYMBOL


class ProdutoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cadastrar Produto")
        self.setFixedSize(480, 480)
        self.setModal(True)
        self.dados = {}
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        container = QFrame()
        container.setObjectName("dialogContainer")
        container.setStyleSheet(f"""
            QFrame#dialogContainer {{
                background-color: {COLORS['white']};
                border-radius: {BORDERS['radius_xl']};
                border: 1px solid {COLORS['gray_100']};
            }}
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 25))
        shadow.setOffset(0, 4)
        container.setGraphicsEffect(shadow)
        
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(32, 32, 32, 32)
        container_layout.setSpacing(24)
        
        header_layout = QHBoxLayout()
        
        icon_label = QLabel("\U0001F4E6")
        icon_label.setStyleSheet("""
            font-size: 32px;
            padding: 0px;
            margin: 0px;
        """)
        header_layout.addWidget(icon_label)
        
        header_text = QVBoxLayout()
        header_text.setSpacing(4)
        
        title = QLabel("Novo Produto")
        title.setStyleSheet(f"""
            font-size: {TYPOGRAPHY['font_size_xl']};
            font-weight: {TYPOGRAPHY['font_weight_bold']};
            color: {COLORS['dark']};
        """)
        
        subtitle = QLabel("Preencha os dados do produto")
        subtitle.setStyleSheet(f"""
            font-size: {TYPOGRAPHY['font_size_sm']};
            color: {COLORS['gray_500']};
        """)
        
        header_text.addWidget(title)
        header_text.addWidget(subtitle)
        header_layout.addLayout(header_text)
        header_layout.addStretch()
        
        container_layout.addLayout(header_layout)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine) # type: ignore
        separator.setStyleSheet(f"""
            QFrame {{
                border: none;
                background-color: {COLORS['gray_100']};
                max-height: 1px;
            }}
        """)
        container_layout.addWidget(separator)
        
        form = QFormLayout()
        form.setSpacing(20)
        form.setLabelAlignment(Qt.AlignLeft) # type: ignore
        
        label_style = f"""
            font-size: {TYPOGRAPHY['font_size_sm']};
            font-weight: {TYPOGRAPHY['font_weight_semibold']};
            color: {COLORS['gray_700']};
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
        """
        
        nome_label = QLabel("Nome do Produto")
        nome_label.setStyleSheet(label_style)
        self.input_nome = QLineEdit()
        self.input_nome.setPlaceholderText("Ex: Arroz Agulha")
        self.input_nome.setFixedHeight(44)
        form.addRow(nome_label, self.input_nome)
        
        categoria_label = QLabel("Categoria")
        categoria_label.setStyleSheet(label_style)
        self.input_categoria = QLineEdit()
        self.input_categoria.setPlaceholderText("Ex: Alimentos, Bebidas, Limpeza")
        self.input_categoria.setFixedHeight(44)
        form.addRow(categoria_label, self.input_categoria)
        
        preco_label = QLabel("Preço Unitário")
        preco_label.setStyleSheet(label_style)
        self.input_preco = QDoubleSpinBox()
        self.input_preco.setRange(0, 999999.99)
        self.input_preco.setPrefix(f"{CURRENCY_SYMBOL} ")
        self.input_preco.setDecimals(2)
        self.input_preco.setFixedHeight(44)
        self.input_preco.setValue(0)
        form.addRow(preco_label, self.input_preco)
        
        estoque_label = QLabel("Estoque Inicial")
        estoque_label.setStyleSheet(label_style)
        self.input_estoque = QSpinBox()
        self.input_estoque.setRange(0, 99999)
        self.input_estoque.setFixedHeight(44)
        self.input_estoque.setValue(0)
        form.addRow(estoque_label, self.input_estoque)
        
        container_layout.addLayout(form)
        container_layout.addStretch()
        
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)
        
        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.setObjectName("cancelBtn")
        self.btn_cancelar.setFixedHeight(44)
        self.btn_cancelar.setCursor(Qt.PointingHandCursor) # type: ignore
        self.btn_cancelar.clicked.connect(self.reject)
        
        self.btn_salvar = QPushButton("Salvar Produto")
        self.btn_salvar.setObjectName("successBtn")
        self.btn_salvar.setFixedHeight(44)
        self.btn_salvar.setCursor(Qt.PointingHandCursor) # type: ignore
        self.btn_salvar.clicked.connect(self.aceitar_dados)
        self.btn_salvar.setDefault(True)
        
        buttons_layout.addWidget(self.btn_cancelar)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.btn_salvar)
        
        container_layout.addLayout(buttons_layout)
        main_layout.addWidget(container)

    def aceitar_dados(self):
        nome = self.input_nome.text().strip()
        categoria = self.input_categoria.text().strip()
        
        if not nome:
            QMessageBox.warning(
                self, 
                "Campo obrigatório",
                "O nome do produto é obrigatório."
            )
            self.input_nome.setFocus()
            return
            
        if not categoria:
            QMessageBox.warning(
                self, 
                "Campo obrigatório",
                "A categoria do produto é obrigatória."
            )
            self.input_categoria.setFocus()
            return
        
        self.dados = {
            'nome': nome,
            'categoria': categoria,
            'preco': self.input_preco.value(),
            'estoque': self.input_estoque.value()
        }
        self.accept()

    def obter_dados(self):
        return self.dados