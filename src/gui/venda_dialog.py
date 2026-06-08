# src/gui/venda_dialog.py
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, 
                               QComboBox, QSpinBox, QDoubleSpinBox,
                               QPushButton, QMessageBox)
from src.gui.styles import get_app_style

class VendaDialog(QDialog):
    def __init__(self, produtos, parent=None):
        super().__init__(parent)
        self.setStyleSheet(get_app_style())
        self.produtos = produtos
        self.setWindowTitle("Registrar Venda")
        self.setFixedSize(350, 200)
        self.dados = {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        form = QFormLayout()

        self.combo_produto = QComboBox()
        for p in self.produtos:
            self.combo_produto.addItem(f"{p.id} - {p.nome}", p.id)
        self.input_qtd = QSpinBox()
        self.input_qtd.setRange(1, 9999)
        self.input_valor_total = QDoubleSpinBox()
        self.input_valor_total.setRange(0, 999999)
        self.input_valor_total.setPrefix("R$ ")

        form.addRow("Produto:", self.combo_produto)
        form.addRow("Quantidade:", self.input_qtd)
        form.addRow("Valor total:", self.input_valor_total)

        self.btn_salvar = QPushButton("Registrar Venda")
        self.btn_salvar.clicked.connect(self.aceitar_dados)

        layout.addLayout(form)
        layout.addWidget(self.btn_salvar)
        self.setLayout(layout)

    def aceitar_dados(self):
        produto_id = self.combo_produto.currentData()
        qtd = self.input_qtd.value()
        total = self.input_valor_total.value()
        if qtd <= 0 or total <= 0:
            QMessageBox.warning(self, "Atenção", "Quantidade e valor total devem ser positivos.")
            return
        self.dados = {
            'produto_id': produto_id,
            'quantidade': qtd,
            'valor_total': total
        }
        self.accept()

    def obter_dados(self):
        return self.dados