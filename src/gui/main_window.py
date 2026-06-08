# src/gui/main_window.py
"""
Janela principal do sistema de inventário com abas de produtos e dashboard de previsão.
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTabWidget, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from src.controllers.inventario_controller import InventarioController
from src.controllers.previsao_controller import PrevisaoController
from src.gui.produto_dialog import ProdutoDialog
from src.gui.venda_dialog import VendaDialog
from src.gui.dashboard_widget import DashboardWidget
from src.gui.styles import get_app_style


class MainWindow(QMainWindow):
    """Janela principal com gestão de produtos, vendas e previsão de demanda."""

    def __init__(self):
        super().__init__()
        # Aplica estilo padrão da aplicação
        self.setStyleSheet(get_app_style())
        self.setWindowTitle("Sistema de Inventário com Previsão de Demanda")
        self.resize(1200, 700)

        # Controllers
        self.inventario_controller = InventarioController()
        self.previsao_controller = PrevisaoController()

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout_principal = QVBoxLayout(self.central_widget)

        # Barra de botões superior
        self.barra_superior = QHBoxLayout()
        self.btn_cadastrar_produto = QPushButton("Cadastrar Produto")
        self.btn_registrar_venda = QPushButton("Registrar Venda")
        self.btn_remover_produto = QPushButton("Eliminar Produto")
        self.btn_atualizar = QPushButton("Atualizar Lista")
        self.btn_recomendar_compra = QPushButton("Recomendar Compra")
        self.barra_superior.addWidget(self.btn_cadastrar_produto)
        self.barra_superior.addWidget(self.btn_remover_produto)
        self.barra_superior.addWidget(self.btn_registrar_venda)
        self.barra_superior.addWidget(self.btn_atualizar)
        self.barra_superior.addWidget(self.btn_recomendar_compra)
        self.barra_superior.addStretch()
        self.layout_principal.addLayout(self.barra_superior)

        self._criar_menu()

        # Abas
        self.tabs = QTabWidget()
        self.tab_produtos = QWidget()
        self.tab_dashboard = DashboardWidget(self.previsao_controller, self.inventario_controller)
        self.tabs.addTab(self.tab_produtos, "Produtos e Estoque")
        self.tabs.addTab(self.tab_dashboard, "Dashboard e Previsão")
        self.layout_principal.addWidget(self.tabs)

        # Tabela de produtos
        self.tabela_produtos = QTableWidget()
        self.tabela_produtos.setColumnCount(6)
        self.tabela_produtos.setHorizontalHeaderLabels(
            ["ID", "Nome", "Categoria", "Preço", "Estoque", "Alerta"]
        )
        self.tabela_produtos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) # pyright: ignore[reportAttributeAccessIssue]
        layout_tab_produtos = QVBoxLayout(self.tab_produtos)
        layout_tab_produtos.addWidget(self.tabela_produtos)

        # Conectar sinais
        self.btn_cadastrar_produto.clicked.connect(self.cadastrar_produto)
        self.btn_registrar_venda.clicked.connect(self.registrar_venda)
        self.btn_recomendar_compra.clicked.connect(self.recomendar_compra)
        self.btn_atualizar.clicked.connect(self.carregar_produtos)
        self.btn_remover_produto.clicked.connect(self.eliminar_produto)

        # Carregar dados iniciais
        self.carregar_produtos()

    def cadastrar_produto(self) -> None:
        """Abre diálogo para cadastrar novo produto."""
        dialog = ProdutoDialog()
        if dialog.exec():
            dados = dialog.obter_dados()
            try:
                self.inventario_controller.cadastrar_produto(
                    nome=dados['nome'],
                    categoria=dados['categoria'],
                    preco=dados['preco'],
                    estoque_inicial=dados['estoque']
                )
                QMessageBox.information(self, "Sucesso", "Produto cadastrado com sucesso!")
                self.carregar_produtos()
                self.tab_dashboard.atualizar_graficos()  # atualiza combo do dashboard
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Falha ao cadastrar produto:\n{str(e)}")

    def registrar_venda(self) -> None:
        """Abre diálogo para registrar venda e atualiza estoque."""
        produtos = self.inventario_controller.listar_produtos()
        if not produtos:
            QMessageBox.warning(self, "Atenção", "Não há produtos cadastrados. Cadastre um produto primeiro.")
            return

        dialog = VendaDialog(produtos)
        if dialog.exec():
            dados = dialog.obter_dados()
            try:
                self.inventario_controller.registrar_venda(
                    produto_id=dados['produto_id'],
                    quantidade=dados['quantidade'],
                    valor_total=dados['valor_total']
                )
                QMessageBox.information(self, "Sucesso", "Venda registrada com sucesso!")
                self.carregar_produtos()
                self.tab_dashboard.atualizar_graficos()  # recarrega combo e limpa gráfico
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Falha ao registrar venda:\n{str(e)}")

    def carregar_produtos(self) -> None:
        """Atualiza a tabela de produtos com os dados do banco."""
        produtos = self.inventario_controller.listar_produtos()
        self.tabela_produtos.setRowCount(len(produtos))

        for i, p in enumerate(produtos):
            # ID
            self.tabela_produtos.setItem(i, 0, QTableWidgetItem(str(p.id)))
            # Nome
            self.tabela_produtos.setItem(i, 1, QTableWidgetItem(p.nome)) # pyright: ignore[reportArgumentType, reportCallIssue]
            # Categoria
            self.tabela_produtos.setItem(i, 2, QTableWidgetItem(p.categoria)) # pyright: ignore[reportArgumentType, reportCallIssue]
            # Preço
            self.tabela_produtos.setItem(i, 3, QTableWidgetItem(f"R$ {p.preco_unitario:.2f}"))
            # Estoque atual
            self.tabela_produtos.setItem(i, 4, QTableWidgetItem(str(p.estoque_atual)))

            # Alerta (simples: considera estoque mínimo + 10 como ponto de pedido)
            ponto_pedido = p.estoque_minimo + 10
            alerta_texto = "Abaixo do ponto de pedido" if p.estoque_atual <= ponto_pedido else "Ok" # pyright: ignore[reportGeneralTypeIssues]
            item_alerta = QTableWidgetItem(alerta_texto)
            if alerta_texto != "Ok":
                item_alerta.setBackground(Qt.GlobalColor.red)
                item_alerta.setForeground(Qt.GlobalColor.white)
            self.tabela_produtos.setItem(i, 5, item_alerta)

        # Ajustar largura das colunas
        self.tabela_produtos.resizeColumnsToContents()

    def _criar_menu(self) -> None:
        arquivo_menu = self.menuBar().addMenu("&Arquivo")
        sair_acao = QAction("Sair", self)
        sair_acao.triggered.connect(self.close)
        arquivo_menu.addAction(sair_acao)

        ajuda_menu = self.menuBar().addMenu("&Ajuda")
        sobre_acao = QAction("Sobre", self)
        sobre_acao.triggered.connect(self.mostrar_sobre)
        ajuda_menu.addAction(sobre_acao)

    def mostrar_sobre(self) -> None:
        QMessageBox.information(
            self,
            "Sobre",
            "Sistema de Inventário Inteligente\nIA de previsão de demanda\nDesenvolvido em Python com PySide6."
        )

    def recomendar_compra(self) -> None:
        recomendacoes = self.inventario_controller.recomendar_compra()
        if not recomendacoes:
            QMessageBox.information(self, "Recomendação", "Nenhuma compra recomendada no momento.")
            return

        mensagens = []
        for item in recomendacoes:
            produto = item['produto']
            mensagens.append(
                f"{produto.nome}: estoque atual {item['estoque_atual']}, "
                f"ponto de pedido {item['ponto_pedido']}, "
                f"quantidade recomendada {item['quantidade_recomendada']}"
            )

        QMessageBox.information(
            self,
            "Recomendação de Compra",
            "\n".join(mensagens)
        )

    def eliminar_produto(self) -> None:
        """Remove o produto selecionado na tabela após confirmação."""
        row = self.tabela_produtos.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Atenção", "Selecione um produto para eliminar.")
            return
        item = self.tabela_produtos.item(row, 0)
        if item is None:
            QMessageBox.warning(self, "Atenção", "Não foi possível identificar o produto selecionado.")
            return
        try:
            produto_id = int(item.text())
        except Exception:
            QMessageBox.warning(self, "Atenção", "ID do produto inválido.")
            return

        resposta = QMessageBox.question(
            self,
            "Confirmar Remoção",
            f"Deseja realmente eliminar o produto ID {produto_id}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if resposta != QMessageBox.Yes:
            return

        try:
            sucesso = self.inventario_controller.remover_produto(produto_id)
            if sucesso:
                QMessageBox.information(self, "Sucesso", "Produto eliminado com sucesso.")
                self.carregar_produtos()
                self.tab_dashboard.atualizar_graficos()
            else:
                QMessageBox.warning(self, "Atenção", "Produto não pôde ser eliminado.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao eliminar produto:\n{str(e)}")

    def closeEvent(self, event) -> None:
        resposta = QMessageBox.question(
            self,
            "Confirmar Saída",
            "Quer realmente sair do sistema?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if resposta == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
