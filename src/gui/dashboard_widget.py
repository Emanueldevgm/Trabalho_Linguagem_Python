# src/gui/dashboard_widget.py
"""
Widget de dashboard para exibir gráficos de vendas e previsão de demanda.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QLabel, QMessageBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas # pyright: ignore[reportPrivateImportUsage]
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
        inventario_controller: InventarioController
    ):
        super().__init__()
        self.setStyleSheet(get_app_style())
        self.previsao_controller = previsao_controller
        self.inventario_controller = inventario_controller
        self.setup_ui()
        self.carregar_produtos_combo()

    def setup_ui(self) -> None:
        """Configura os elementos da interface."""
        layout = QVBoxLayout()

        # Barra de seleção e botão
        sel_layout = QHBoxLayout()
        self.label_produto = QLabel("Produto:")
        self.combo_produtos = QComboBox()
        self.btn_prever = QPushButton("Gerar Previsão de Demanda")
        self.btn_prever.clicked.connect(self.gerar_previsao)

        sel_layout.addWidget(self.label_produto)
        sel_layout.addWidget(self.combo_produtos)
        sel_layout.addWidget(self.btn_prever)
        sel_layout.addStretch()
        layout.addLayout(sel_layout)

        self.label_metricas = QLabel("")
        layout.addWidget(self.label_metricas)

        # Canvas para gráfico matplotlib
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

    def gerar_previsao(self) -> None:
        """Dispara o processo de previsão e exibe o gráfico."""
        produto_id = self.combo_produtos.currentData()
        if not produto_id:
            QMessageBox.warning(self, "Atenção", "Selecione um produto.")
            return

        try:
            # Gera a previsão para os próximos 30 dias
            previsao_df, metricas = self.previsao_controller.gerar_previsao(produto_id, dias_futuros=30)

            # Obtém o histórico real dos últimos 60 dias
            historico = self.previsao_controller.venda_repo.obter_historico_por_produto(
                produto_id, dias=60
            )

            self.plotar_grafico(historico, previsao_df, metricas)

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
        metricas: Optional[dict] = None
    ) -> None:
        """Plota as vendas históricas e a previsão no mesmo gráfico."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Valida e plota histórico
        if not historico.empty and 'data' in historico.columns and 'quantidade' in historico.columns:
            datas_hist = pd.to_datetime(historico['data'])
            ax.plot(datas_hist, historico['quantidade'], 'o-', label='Vendas reais', linewidth=2)

        # Valida e plota previsão
        if not previsao.empty and 'data_previsao' in previsao.columns and 'quantidade_prevista' in previsao.columns:
            datas_prev = pd.to_datetime(previsao['data_previsao'])
            ax.plot(datas_prev, previsao['quantidade_prevista'], 's--', label='Previsão (30 dias)', linewidth=2)

        # Configurações estéticas
        ax.set_title("Demanda Histórica e Previsão de Demanda (IA)", fontsize=12)
        ax.set_xlabel("Data")
        ax.set_ylabel("Quantidade Vendida")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7)
        self.figure.tight_layout()
        self.canvas.draw()

        if metricas:
            self.label_metricas.setText(
                f"RMSE: {metricas['rmse']:.2f}   MAE: {metricas['mae']:.2f}"
            )
        else:
            self.label_metricas.setText("")

    def atualizar_graficos(self) -> None:
        """Recarrega a lista de produtos e limpa o gráfico."""
        self.carregar_produtos_combo()
        self.figure.clear()
        self.canvas.draw()