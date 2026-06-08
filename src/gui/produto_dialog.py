# src/gui/produto_dialog.py
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, 
                               QLineEdit, QDoubleSpinBox, QSpinBox,
                               QPushButton, QMessageBox)
from src.gui.styles import get_app_style

class ProdutoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(get_app_style())
        self.setWindowTitle("Cadastrar Produto")
        self.setFixedSize(350, 250)
        self.dados = {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        form = QFormLayout()

        self.input_nome = QLineEdit()
        self.input_categoria = QLineEdit()
        self.input_preco = QDoubleSpinBox()
        self.input_preco.setRange(0, 99999)
        self.input_preco.setPrefix("R$ ")
        self.input_estoque = QSpinBox()
        self.input_estoque.setRange(0, 10000)

        form.addRow("Nome:", self.input_nome)
        form.addRow("Categoria:", self.input_categoria)
        form.addRow("Preço unitário:", self.input_preco)
        form.addRow("Estoque inicial:", self.input_estoque)

        self.btn_salvar = QPushButton("Salvar")
        self.btn_salvar.clicked.connect(self.aceitar_dados)

        layout.addLayout(form)
        layout.addWidget(self.btn_salvar)
        self.setLayout(layout)

    def aceitar_dados(self):
        if not self.input_nome.text() or not self.input_categoria.text():
            QMessageBox.warning(self, "Atenção", "Nome e categoria são obrigatórios.")
            return
        self.dados = {
            'nome': self.input_nome.text(),
            'categoria': self.input_categoria.text(),
            'preco': self.input_preco.value(),
            'estoque': self.input_estoque.value()
        }
        self.accept()

    def obter_dados(self):
        return self.dados