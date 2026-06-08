def get_app_style() -> str:
    """Retorna o stylesheet padrão da aplicação para ser aplicado em janelas e widgets."""
    return """
    QDialog, QWidget { background-color: #ffffff; color: #000000; }
    QLabel { font-size: 12px; color: #000000; }
    QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox { background: white; border: 1px solid #cfd8dc; border-radius: 6px; padding-left: 8px; color: #000000; }
    QLineEdit::placeholder { color: #9e9e9e; }
    QPushButton { background-color: #1976d2; color: white; padding: 8px 14px; border-radius: 6px; }
    QPushButton#cancel { background-color: #9e9e9e; color: white; }
    QPushButton:hover { background-color: #1565c0; }

    /* Tabs (Produtos / Estoque / Dashboard) */
    QTabBar::tab { background: #e3f2fd; padding: 8px 14px; border-radius: 6px; margin-right: 4px; color: #0d47a1; }
    QTabBar::tab:selected { background: #1976d2; color: white; }
    QTabBar::tab:hover { background: #1565c0; color: white; }
    QTabWidget::pane { border: 1px solid #cfd8dc; border-radius: 6px; }

    QCheckBox { padding: 4px; color: #000000; }
    QVBoxLayout { margin: 12px; }
    """
