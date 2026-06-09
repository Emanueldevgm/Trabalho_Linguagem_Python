                             
"""
Widget de dashboard para exibir gráficos de vendas e previsão de demanda.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QLabel, QMessageBox,
    QInputDialog
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas                                             # pyright: ignore[reportPrivateImportUsage]
from matplotlib.figure import Figure
import pandas as pd
from typing import Optional

from src.controllers.previsao_controller import PrevisaoController
from src.controllers.inventario_controller import InventarioController
from src.gui.styles import get_app_style


class DashboardWidget(QWidget):
    """Widget com gráficos de demanda histórica e previsão de IA."""

    def __init__(
        self,
        previsao_controller: PrevisaoController,
        inventario_controller: InventarioController,
        ia_controller: "IAController" # pyright: ignore[reportUndefinedVariable]
    ):
        super().__init__()
        self.setStyleSheet(get_app_style())
        self.previsao_controller = previsao_controller
        self.inventario_controller = inventario_controller
        self.ia_controller = ia_controller
        self.setup_ui()
        self.carregar_produtos_combo()

    def setup_ui(self) -> None:
        """Configura os elementos da interface."""
        layout = QVBoxLayout()

                                  
        sel_layout = QHBoxLayout()
        self.label_produto = QLabel("Produto:")
        self.combo_produtos = QComboBox()
        self.combo_produtos.currentIndexChanged.connect(self.on_produto_trocado)
        self.btn_prever = QPushButton("Gerar Previsão de Demanda")
        self.btn_prever.clicked.connect(self.gerar_previsao)

        self.btn_classificar = QPushButton("Classificar Demanda")
        self.btn_classificar.clicked.connect(self.classificar_demanda)

        self.btn_sentimento = QPushButton("Analisar Feedback")
        self.btn_sentimento.clicked.connect(self.analisar_feedback)

        sel_layout.addWidget(self.label_produto)
        sel_layout.addWidget(self.combo_produtos)
        sel_layout.addWidget(self.btn_prever)
        sel_layout.addWidget(self.btn_classificar)
        sel_layout.addWidget(self.btn_sentimento)
        sel_layout.addStretch()
        layout.addLayout(sel_layout)

        self.label_metricas = QLabel("")
        self.label_metricas.setWordWrap(True)
        layout.addWidget(self.label_metricas)

        self.figure = Figure(figsize=(8, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def carregar_produtos_combo(self) -> None:
        """Carrega a lista de produtos no combobox."""
        produtos = self.inventario_controller.listar_produtos()
        self.combo_produtos.clear()
        for p in produtos:
            self.combo_produtos.addItem(f"{p.nome} (ID: {p.id})", p.id)

        if self.combo_produtos.count() > 0:
            self.combo_produtos.setCurrentIndex(0)
            self.atualizar_dashboard_inicial()

    def on_produto_trocado(self, index: int) -> None:
        if index >= 0:
            self.atualizar_dashboard_inicial()

    def atualizar_dashboard_inicial(self) -> None:
        produto_id = self.combo_produtos.currentData()
        if not produto_id:
            self.figure.clear()
            self.canvas.draw()
            self.label_metricas.setText("Nenhum produto selecionado.")
            return

        historico = self.previsao_controller.venda_repo.obter_historico_por_produto(
            produto_id, dias=90
        )

        if len(historico) < 2:
            self.figure.clear()
            self.canvas.draw()
            self.label_metricas.setText(
                "É necessário pelo menos 2 registros de vendas para exibir o gráfico histórico. "
                "Registre mais vendas e tente novamente."
            )
            return

        self.plotar_grafico(historico, pd.DataFrame(), None, None)
        self.label_metricas.setText(
            "Gráfico de vendas históricas carregado. "
            "Clique em Gerar Previsão para ver a previsão de demanda."
        )

    def gerar_previsao(self) -> None:
        """Dispara o processo de previsão e exibe o gráfico."""
        produto_id = self.combo_produtos.currentData()
        if not produto_id:
            QMessageBox.warning(self, "Atenção", "Selecione um produto.")
            return

        try:
            previsao_df, metricas = self.previsao_controller.gerar_previsao(produto_id, dias_futuros=30)
            metricas_inventario = self.inventario_controller.obter_metricas_inventario(produto_id, dias=30)

            historico = self.previsao_controller.venda_repo.obter_historico_por_produto(
                produto_id, dias=60
            )

            self.plotar_grafico(historico, previsao_df, metricas, metricas_inventario)
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erro na Previsão",
                f"Não foi possível gerar a previsão:\n{str(e)}"
            )

    def plotar_grafico(
        self,
        historico: pd.DataFrame,
        previsao: pd.DataFrame,
        metricas: Optional[dict] = None,
        metricas_inventario: Optional[dict] = None
    ) -> None:
        """Plota as vendas históricas, a previsão e mostra as métricas calculadas."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)

                                  
        if not historico.empty and 'data' in historico.columns and 'quantidade' in historico.columns:
            datas_hist = pd.to_datetime(historico['data'])
            ax.plot(datas_hist, historico['quantidade'], 'o-', label='Vendas reais', linewidth=2)

                                 
        if not previsao.empty and 'data_previsao' in previsao.columns and 'quantidade_prevista' in previsao.columns:
            datas_prev = pd.to_datetime(previsao['data_previsao'])
            ax.plot(datas_prev, previsao['quantidade_prevista'], 's--', label='Previsão (30 dias)', linewidth=2)

                                 
        ax.set_title("Demanda Histórica e Previsão de Demanda (IA)", fontsize=12)
        ax.set_xlabel("Data")
        ax.set_ylabel("Quantidade Vendida")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7)
        self.figure.tight_layout()
        self.canvas.draw()

        if metricas:
            dias_estoque = metricas_inventario.get('dias_estoque', float('inf')) if metricas_inventario else float('inf')
            dias_estoque_text = "∞" if dias_estoque == float('inf') else f"{dias_estoque:.1f}"
            estoque_text = (
                f"Média diária: {metricas_inventario['media_diaria']:.2f} unidades | "
                f"Dias de estoque: {dias_estoque_text} | "
                f"Ponto de pedido: {metricas_inventario['ponto_pedido']} | "
                f"Reposição recomendada: {metricas_inventario['quantidade_recomendada']}"
            ) if metricas_inventario else ""
            self.label_metricas.setText(
                f"RMSE: {metricas['rmse']:.2f}   MAE: {metricas['mae']:.2f}\n{estoque_text}"
            )
        else:
            self.label_metricas.setText("")

    def classificar_demanda(self) -> None:
        produto_id = self.combo_produtos.currentData()
        if not produto_id:
            QMessageBox.warning(self, "Atenção", "Selecione um produto.")
            return

        try:
            resultado = self.ia_controller.classificar_demanda(produto_id)
            probabilidades = "\n".join(
                f"{classe}: {prob:.2%}"
                for classe, prob in resultado["probabilidades"].items()
            )
            QMessageBox.information(
                self,
                "Classificação de Demanda",
                (
                    f"Classe prevista: {resultado['classe_prevista']}\n"
                    f"Status do modelo: {resultado['modelo_status']}\n\n"
                    f"Probabilidades:\n{probabilidades}"
                )
            )
        except Exception as e:
            QMessageBox.critical(self, "Erro de Classificação", str(e))

    def analisar_feedback(self) -> None:
        texto, ok = QInputDialog.getMultiLineText(
            self,
            "Análise de Sentimento",
            "Digite o feedback do cliente:",
            ""
        )
        if not ok or not texto.strip():
            return

        try:
            resultado = self.ia_controller.analisar_feedback(texto)
            probabilidades = "\n".join(
                f"{classe}: {prob:.2%}"
                for classe, prob in resultado["probabilidades"].items()
            )
            QMessageBox.information(
                self,
                "Resultado de Sentimento",
                (
                    f"Texto: {resultado['texto']}\n"
                    f"Sentimento: {resultado['sentimento']}\n"
                    f"Status do modelo: {resultado['modelo_status']}\n\n"
                    f"Probabilidades:\n{probabilidades}"
                )
            )
        except Exception as e:
            QMessageBox.critical(self, "Erro de Sentimento", str(e))

    def atualizar_graficos(self) -> None:
        """Recarrega a lista de produtos e limpa o gráfico."""
        self.carregar_produtos_combo()
        self.figure.clear()
        self.canvas.draw()