from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QComboBox, QSpinBox, QDoubleSpinBox,
    QPushButton, QLabel, QMessageBox, QFrame,
    QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from src.gui.styles import COLORS, TYPOGRAPHY, BORDERS
from src.utils.constants import CURRENCY_SYMBOL


class VendaDialog(QDialog):
    def __init__(self, produtos, parent=None):
        super().__init__(parent)
        self.produtos = produtos
        self.setWindowTitle("Registrar Venda")
        self.setFixedSize(480, 430)
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
        
        icon_label = QLabel("\U0001F4B0")
        icon_label.setStyleSheet("""
            font-size: 32px;
            padding: 0px;
            margin: 0px;
        """)
        header_layout.addWidget(icon_label)
        
        header_text = QVBoxLayout()
        header_text.setSpacing(4)
        
        title = QLabel("Nova Venda")
        title.setStyleSheet(f"""
            font-size: {TYPOGRAPHY['font_size_xl']};
            font-weight: {TYPOGRAPHY['font_weight_bold']};
            color: {COLORS['dark']};
        """)
        
        subtitle = QLabel("Registre a venda realizada")
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
        
        produto_label = QLabel("Produto")
        produto_label.setStyleSheet(label_style)
        self.combo_produto = QComboBox()
        self.combo_produto.setFixedHeight(44)
        for p in self.produtos:
            self.combo_produto.addItem(
                f"{p.nome} - Estoque: {p.estoque_atual} un.", 
                p.id
            )
        self.combo_produto.currentIndexChanged.connect(self.atualizar_valor_sugerido)
        form.addRow(produto_label, self.combo_produto)
        
        quantidade_label = QLabel("Quantidade Vendida")
        quantidade_label.setStyleSheet(label_style)
        self.input_qtd = QSpinBox()
        self.input_qtd.setRange(1, 99999)
        self.input_qtd.setFixedHeight(44)
        self.input_qtd.setValue(1)
        self.input_qtd.valueChanged.connect(self.atualizar_valor_sugerido)
        form.addRow(quantidade_label, self.input_qtd)
        
        valor_label = QLabel("Valor Total da Venda")
        valor_label.setStyleSheet(label_style)
        self.input_valor_total = QDoubleSpinBox()
        self.input_valor_total.setRange(0.01, 999999.99)
        self.input_valor_total.setPrefix(f"{CURRENCY_SYMBOL} ")
        self.input_valor_total.setDecimals(2)
        self.input_valor_total.setFixedHeight(44)
        self.input_valor_total.setValue(0)
        form.addRow(valor_label, self.input_valor_total)
        
        container_layout.addLayout(form)
        
        info_layout = QHBoxLayout()
        self.label_sugestao = QLabel("")
        self.label_sugestao.setStyleSheet(f"""
            font-size: {TYPOGRAPHY['font_size_sm']};
            color: {COLORS['gray_500']};
            font-style: italic;
            padding: 8px 0px;
        """)
        info_layout.addWidget(self.label_sugestao)
        info_layout.addStretch()
        container_layout.addLayout(info_layout)
        
        container_layout.addStretch()
        
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)
        
        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.setObjectName("cancelBtn")
        self.btn_cancelar.setFixedHeight(44)
        self.btn_cancelar.setCursor(Qt.PointingHandCursor) # type: ignore
        self.btn_cancelar.clicked.connect(self.reject)
        
        self.btn_salvar = QPushButton("Registrar Venda")
        self.btn_salvar.setFixedHeight(44)
        self.btn_salvar.setCursor(Qt.PointingHandCursor) # type: ignore
        self.btn_salvar.clicked.connect(self.aceitar_dados)
        self.btn_salvar.setDefault(True)
        
        buttons_layout.addWidget(self.btn_cancelar)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.btn_salvar)
        
        container_layout.addLayout(buttons_layout)
        main_layout.addWidget(container)
        
        self.atualizar_valor_sugerido()

    def atualizar_valor_sugerido(self):
        produto_id = self.combo_produto.currentData()
        quantidade = self.input_qtd.value()
        
        if produto_id and quantidade > 0:
            for p in self.produtos:
                if p.id == produto_id:
                    valor_sugerido = p.preco_unitario * quantidade
                    self.label_sugestao.setText(
                        f"Valor sugerido: {CURRENCY_SYMBOL} {valor_sugerido:,.2f}"
                    )
                    if self.input_valor_total.value() == 0:
                        self.input_valor_total.setValue(valor_sugerido)
                    break

    def aceitar_dados(self):
        produto_id = self.combo_produto.currentData()
        quantidade = self.input_qtd.value()
        valor_total = self.input_valor_total.value()
        
        if not produto_id:
            QMessageBox.warning(
                self, 
                "Selecione um produto",
                "Por favor, selecione um produto para a venda."
            )
            return
        
        if quantidade <= 0:
            QMessageBox.warning(
                self, 
                "Quantidade inválida",
                "A quantidade deve ser maior que zero."
            )
            self.input_qtd.setFocus()
            return
        
        if valor_total <= 0:
            QMessageBox.warning(
                self, 
                "Valor inválido",
                "O valor total deve ser maior que zero."
            )
            self.input_valor_total.setFocus()
            return
        
        produto = None
        for p in self.produtos:
            if p.id == produto_id:
                produto = p
                break
        
        if produto and quantidade > produto.estoque_atual:
            resposta = QMessageBox.question(
                self,
                "Estoque insuficiente",
                f"O produto '{produto.nome}' possui apenas {produto.estoque_atual} unidades em estoque.\n"
                f"Você está tentando vender {quantidade} unidades.\n\n"
                "Deseja continuar mesmo assim?",
                QMessageBox.Yes | QMessageBox.No, # type: ignore
                QMessageBox.No # type: ignore
            )
            if resposta == QMessageBox.No: # type: ignore
                return
        
        self.dados = {
            'produto_id': produto_id,
            'quantidade': quantidade,
            'valor_total': valor_total
        }
        self.accept()

    def obter_dados(self):
        return self.dados