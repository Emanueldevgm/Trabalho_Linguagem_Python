from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTabWidget, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QLabel, QFrame, QStatusBar,
    QToolBar, QSizePolicy
)
from PySide6.QtGui import QAction, QColor
from PySide6.QtCore import Qt, QTimer
from src.controllers.inventario_controller import InventarioController
from src.controllers.previsao_controller import PrevisaoController
from src.gui.produto_dialog import ProdutoDialog
from src.gui.venda_dialog import VendaDialog
from src.gui.dashboard_widget import DashboardWidget
from src.gui.styles import get_app_style, COLORS, TYPOGRAPHY, BORDERS
from src.utils.constants import format_currency
import datetime


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(get_app_style())
        self.setWindowTitle("Inventário IA")
        self.resize(1280, 800)
        self.setMinimumSize(1024, 680)

        self.inventario_controller = InventarioController()
        self.previsao_controller = PrevisaoController()

        self._criar_toolbar()
        self._criar_widget_central()
        self._criar_menu()
        self._criar_statusbar()
        
        self.carregar_produtos()
        QTimer.singleShot(100, self._atualizar_status)

    def _criar_toolbar(self):
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setStyleSheet(f"""
            QToolBar {{
                background-color: {COLORS['white']};
                border-bottom: 1px solid {COLORS['gray_100']};
                padding: 8px 16px;
                spacing: 8px;
            }}
        """)
        
        self.toolbar_title = QLabel("Inventário IA")
        self.toolbar_title.setStyleSheet(f"""
            font-size: {TYPOGRAPHY['font_size_xl']};
            font-weight: {TYPOGRAPHY['font_weight_bold']};
            color: {COLORS['dark']};
            margin-right: 24px;
        """)
        toolbar.addWidget(self.toolbar_title)
        toolbar.addSeparator()
        
        self.btn_novo_produto = QPushButton("+ Novo Produto")
        self.btn_novo_produto.setObjectName("successBtn")
        self.btn_novo_produto.setCursor(Qt.PointingHandCursor) # type: ignore
        self.btn_novo_produto.clicked.connect(self.cadastrar_produto)
        toolbar.addWidget(self.btn_novo_produto)
        
        self.btn_nova_venda = QPushButton("$ Registrar Venda")
        self.btn_nova_venda.setCursor(Qt.PointingHandCursor) # type: ignore
        self.btn_nova_venda.clicked.connect(self.registrar_venda)
        toolbar.addWidget(self.btn_nova_venda)
        
        self.btn_recomendar = QPushButton("Recomendar Compra")
        self.btn_recomendar.setObjectName("secondaryBtn")
        self.btn_recomendar.setCursor(Qt.PointingHandCursor) # type: ignore
        self.btn_recomendar.clicked.connect(self.recomendar_compra)
        toolbar.addWidget(self.btn_recomendar)
        
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred) # type: ignore
        toolbar.addWidget(spacer)
        
        self.btn_atualizar = QPushButton("Atualizar")
        self.btn_atualizar.setObjectName("secondaryBtn")
        self.btn_atualizar.setCursor(Qt.PointingHandCursor) # type: ignore
        self.btn_atualizar.clicked.connect(self.carregar_produtos)
        toolbar.addWidget(self.btn_atualizar)
        
        self.addToolBar(toolbar)

    def _criar_widget_central(self):
        central = QWidget()
        central.setObjectName("centralWidget")
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(24)
        
        header = QFrame()
        header.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {COLORS['primary']}, stop:1 {COLORS['primary_dark']});
                border-radius: {BORDERS['radius_lg']};
                padding: 24px;
            }}
        """)
        
        header_layout = QVBoxLayout(header)
        header_layout.setSpacing(8)
        
        welcome_label = QLabel("Bem-vindo ao Sistema de Gestão de Inventário")
        welcome_label.setStyleSheet(f"""
            color: white;
            font-size: {TYPOGRAPHY['font_size_2xl']};
            font-weight: {TYPOGRAPHY['font_weight_bold']};
        """)
        header_layout.addWidget(welcome_label)
        
        date_label = QLabel(datetime.datetime.now().strftime("%d de %B de %Y"))
        date_label.setStyleSheet(f"""
            color: rgba(255, 255, 255, 0.8);
            font-size: {TYPOGRAPHY['font_size_lg']};
        """)
        header_layout.addWidget(date_label)
        
        main_layout.addWidget(header)
        
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        
        self.tab_produtos = QWidget()
        self.tab_dashboard = DashboardWidget(self.previsao_controller, self.inventario_controller)
        
        self.tabs.addTab(self.tab_produtos, "Produtos & Estoque")
        self.tabs.addTab(self.tab_dashboard, "Dashboard & Previsão")
        
        self.tabela_produtos = QTableWidget()
        self.tabela_produtos.setColumnCount(7)
        self.tabela_produtos.setHorizontalHeaderLabels([
            "ID", "Produto", "Categoria", "Preço Unitário", 
            "Estoque Atual", "Estado", "Ações"
        ])
        self.tabela_produtos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) # type: ignore
        self.tabela_produtos.setSelectionBehavior(QTableWidget.SelectRows) # type: ignore
        self.tabela_produtos.setAlternatingRowColors(True)
        self.tabela_produtos.setShowGrid(False)
        self.tabela_produtos.verticalHeader().setVisible(False)
        self.tabela_produtos.setCursor(Qt.PointingHandCursor) # type: ignore
        
        tabela_layout = QVBoxLayout(self.tab_produtos)
        tabela_layout.setContentsMargins(0, 16, 0, 0)
        tabela_layout.addWidget(self.tabela_produtos)
        
        main_layout.addWidget(self.tabs)

    def _criar_menu(self):
        menubar = self.menuBar()
        
        arquivo_menu = menubar.addMenu("Arquivo")
        
        novo_action = QAction("Novo Produto", self)
        novo_action.setShortcut("Ctrl+N")
        novo_action.triggered.connect(self.cadastrar_produto)
        arquivo_menu.addAction(novo_action)
        
        venda_action = QAction("Registrar Venda", self)
        venda_action.setShortcut("Ctrl+V")
        venda_action.triggered.connect(self.registrar_venda)
        arquivo_menu.addAction(venda_action)
        
        arquivo_menu.addSeparator()
        
        sair_action = QAction("Sair", self)
        sair_action.setShortcut("Ctrl+Q")
        sair_action.triggered.connect(self.close)
        arquivo_menu.addAction(sair_action)
        
        ajuda_menu = menubar.addMenu("Ajuda")
        sobre_action = QAction("Sobre o Sistema", self)
        sobre_action.triggered.connect(self.mostrar_sobre)
        ajuda_menu.addAction(sobre_action)

    def _criar_statusbar(self):
        self.statusbar = QStatusBar()
        self.statusbar.setStyleSheet(f"""
            QStatusBar {{
                background-color: {COLORS['white']};
                border-top: 1px solid {COLORS['gray_100']};
                color: {COLORS['gray_500']};
                font-size: {TYPOGRAPHY['font_size_sm']};
                padding: 4px 16px;
            }}
        """)
        self.setStatusBar(self.statusbar)

    def _atualizar_status(self):
        produtos = self.inventario_controller.listar_produtos()
        total_produtos = len(produtos)
        total_estoque = sum(p.estoque_atual for p in produtos)
        alertas = sum(1 for p in produtos if p.estoque_atual <= (p.estoque_minimo + 10)) # type: ignore
        
        self.statusbar.showMessage(
            f"Total de Produtos: {total_produtos} | "
            f"Itens em Estoque: {total_estoque} | "
            f"Alertas de Estoque Baixo: {alertas}"
        )

    def cadastrar_produto(self):
        dialog = ProdutoDialog(self)
        if dialog.exec():
            dados = dialog.obter_dados()
            try:
                self.inventario_controller.cadastrar_produto(
                    nome=dados['nome'],
                    categoria=dados['categoria'],
                    preco=dados['preco'],
                    estoque_inicial=dados['estoque']
                )
                QMessageBox.information(self, "Produto cadastrado", 
                    f"O produto '{dados['nome']}' foi cadastrado com sucesso.")
                self.carregar_produtos()
                self.tab_dashboard.atualizar_graficos()
                self._atualizar_status()
            except Exception as e:
                QMessageBox.critical(self, "Erro ao cadastrar", str(e))

    def registrar_venda(self):
        produtos = self.inventario_controller.listar_produtos()
        if not produtos:
            QMessageBox.warning(self, "Sem produtos", 
                "Cadastre pelo menos um produto antes de registrar vendas.")
            return

        dialog = VendaDialog(produtos, self)
        if dialog.exec():
            dados = dialog.obter_dados()
            try:
                self.inventario_controller.registrar_venda(
                    produto_id=dados['produto_id'],
                    quantidade=dados['quantidade'],
                    valor_total=dados['valor_total']
                )
                QMessageBox.information(self, "Venda registrada", 
                    "A venda foi registrada com sucesso.")
                self.carregar_produtos()
                self.tab_dashboard.atualizar_graficos()
                self._atualizar_status()
            except Exception as e:
                QMessageBox.critical(self, "Erro ao registrar", str(e))

    def carregar_produtos(self):
        produtos = self.inventario_controller.listar_produtos()
        self.tabela_produtos.setRowCount(len(produtos))

        for i, p in enumerate(produtos):
            self.tabela_produtos.setItem(i, 0, QTableWidgetItem(str(p.id)))
            self.tabela_produtos.setItem(i, 1, QTableWidgetItem(p.nome)) # type: ignore
            self.tabela_produtos.setItem(i, 2, QTableWidgetItem(p.categoria)) # type: ignore
            self.tabela_produtos.setItem(i, 3, QTableWidgetItem(format_currency(p.preco_unitario))) # type: ignore
            self.tabela_produtos.setItem(i, 4, QTableWidgetItem(str(p.estoque_atual)))
            
            ponto_pedido = p.estoque_minimo + 10
            
            if p.estoque_atual == 0: # type: ignore
                status = "Esgotado"
                status_widget = QLabel(status)
                status_widget.setObjectName("statusAlert")
            elif p.estoque_atual <= ponto_pedido: # type: ignore
                status = "Baixo"
                status_widget = QLabel(status)
                status_widget.setObjectName("statusWarning")
            else:
                status = "Normal"
                status_widget = QLabel(status)
                status_widget.setObjectName("statusOk")
            
            status_widget.setAlignment(Qt.AlignCenter) # type: ignore
            self.tabela_produtos.setCellWidget(i, 5, status_widget)
            
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(4, 4, 4, 4)
            actions_layout.setSpacing(4)
            
            vender_btn = QPushButton("Vender")
            vender_btn.setObjectName("successBtn")
            vender_btn.setFixedWidth(70)
            vender_btn.setCursor(Qt.PointingHandCursor) # type: ignore
            vender_btn.clicked.connect(lambda checked, pid=p.id: self._vender_produto_rapido(pid))
            
            remover_btn = QPushButton("Remover")
            remover_btn.setObjectName("dangerBtn")
            remover_btn.setFixedWidth(70)
            remover_btn.setCursor(Qt.PointingHandCursor) # type: ignore
            remover_btn.clicked.connect(lambda checked, pid=p.id: self._remover_produto_rapido(pid))
            
            actions_layout.addWidget(vender_btn)
            actions_layout.addWidget(remover_btn)
            actions_layout.addStretch()
            
            self.tabela_produtos.setCellWidget(i, 6, actions_widget)
            self.tabela_produtos.setRowHeight(i, 50)
        
        self.tabela_produtos.resizeColumnsToContents()
        self.tabela_produtos.setColumnWidth(0, 60)
        self.tabela_produtos.setColumnWidth(5, 120)
        self.tabela_produtos.setColumnWidth(6, 160)

    def _vender_produto_rapido(self, produto_id):
        produtos = self.inventario_controller.listar_produtos()
        produto_encontrado = None
        for p in produtos:
            if p.id == produto_id:
                produto_encontrado = p
                break
        
        if produto_encontrado:
            dialog = VendaDialog([produto_encontrado], self)
            if dialog.exec():
                dados = dialog.obter_dados()
                try:
                    self.inventario_controller.registrar_venda(
                        produto_id=dados['produto_id'],
                        quantidade=dados['quantidade'],
                        valor_total=dados['valor_total']
                    )
                    self.carregar_produtos()
                    self.tab_dashboard.atualizar_graficos()
                    self._atualizar_status()
                except Exception as e:
                    QMessageBox.critical(self, "Erro", str(e))

    def _remover_produto_rapido(self, produto_id):
        resposta = QMessageBox.question(
            self,
            "Confirmar remoção",
            f"Tem certeza que deseja remover o produto ID {produto_id}?",
            QMessageBox.Yes | QMessageBox.No, # type: ignore
            QMessageBox.No # type: ignore
        )
        
        if resposta == QMessageBox.Yes: # type: ignore
            try:
                sucesso = self.inventario_controller.remover_produto(produto_id)
                if sucesso:
                    self.carregar_produtos()
                    self.tab_dashboard.atualizar_graficos()
                    self._atualizar_status()
                    self.statusbar.showMessage("Produto removido com sucesso", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Erro ao remover", str(e))

    def recomendar_compra(self):
        self.statusbar.showMessage("Calculando recomendações...")
        recomendacoes = self.inventario_controller.recomendar_compra()
        
        if not recomendacoes:
            QMessageBox.information(self, "Estoque adequado", 
                "Todos os produtos estão com estoque adequado.")
            self.statusbar.showMessage("Pronto", 3000)
            return

        mensagem = "Produtos que precisam de reposição:\n\n"
        for item in recomendacoes:
            produto = item['produto']
            mensagem += (
                f"• {produto.nome}\n"
                f"  Estoque atual: {item['estoque_atual']} unidades\n"
                f"  Ponto de pedido: {item['ponto_pedido']} unidades\n"
                f"  Quantidade recomendada: {item['quantidade_recomendada']} unidades\n\n"
            )
        
        QMessageBox.information(self, "Recomendações de Compra", mensagem)
        self.statusbar.showMessage(f"{len(recomendacoes)} produto(s) precisam de reposição", 5000)

    def mostrar_sobre(self):
        QMessageBox.about(
            self,
            "Sobre o Inventário IA",
            "<h3>Inventário IA</h3>"
            "<p>Sistema Inteligente de Gestão de Inventário</p>"
            "<p>Versão 1.0.0</p>"
            "<br>"
            "<p>Desenvolvido com Python e PySide6</p>"
            "<p>Previsão de demanda com Machine Learning</p>"
        )

    def closeEvent(self, event):
        resposta = QMessageBox.question(
            self,
            "Confirmar saída",
            "Deseja realmente sair do sistema?",
            QMessageBox.Yes | QMessageBox.No, # type: ignore
            QMessageBox.No # type: ignore
        )
        
        if resposta == QMessageBox.Yes: # type: ignore
            event.accept()
        else:
            event.ignore()