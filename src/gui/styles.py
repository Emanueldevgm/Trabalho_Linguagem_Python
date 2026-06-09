from PySide6.QtCore import Qt

COLORS = {
    'primary': '#2563EB',
    'primary_dark': '#1D4ED8',
    'primary_light': '#DBEAFE',
    'secondary': '#059669',
    'secondary_light': '#D1FAE5',
    'danger': '#DC2626',
    'danger_light': '#FEE2E2',
    'warning': '#D97706',
    'warning_light': '#FEF3C7',
    'success': '#059669',
    'info': '#0891B2',
    'dark': '#111827',
    'gray_900': '#1F2937',
    'gray_700': '#374151',
    'gray_500': '#6B7280',
    'gray_300': '#D1D5DB',
    'gray_100': '#F3F4F6',
    'gray_50': '#F9FAFB',
    'white': '#FFFFFF',
    'black': '#000000',
}

SPACING = {
    'xs': '4px',
    'sm': '8px',
    'md': '16px',
    'lg': '24px',
    'xl': '32px',
    '2xl': '48px',
    '3xl': '64px',
}

TYPOGRAPHY = {
    'font_family': 'Segoe UI, -apple-system, system-ui, sans-serif',
    'font_size_sm': '11px',
    'font_size_base': '13px',
    'font_size_lg': '15px',
    'font_size_xl': '18px',
    'font_size_2xl': '24px',
    'font_size_3xl': '32px',
    'font_weight_normal': '400',
    'font_weight_medium': '500',
    'font_weight_semibold': '600',
    'font_weight_bold': '700',
    'line_height_tight': '1.25',
    'line_height_normal': '1.5',
}

BORDERS = {
    'radius_sm': '4px',
    'radius_md': '8px',
    'radius_lg': '12px',
    'radius_xl': '16px',
    'radius_full': '9999px',
    'width_thin': '1px',
    'width_normal': '1.5px',
    'width_thick': '2px',
}

SHADOWS = {
    'sm': '0 1px 2px rgba(0, 0, 0, 0.05)',
    'md': '0 4px 6px rgba(0, 0, 0, 0.07)',
    'lg': '0 10px 15px rgba(0, 0, 0, 0.1)',
    'xl': '0 20px 25px rgba(0, 0, 0, 0.15)',
}

def get_app_style():
    return f"""
    * {{
        font-family: {TYPOGRAPHY['font_family']};
        font-size: {TYPOGRAPHY['font_size_base']};
        line-height: {TYPOGRAPHY['line_height_normal']};
    }}

    QMainWindow {{
        background-color: {COLORS['gray_50']};
    }}

    QDialog {{
        background-color: {COLORS['white']};
        border-radius: {BORDERS['radius_lg']};
    }}

    QWidget#centralWidget {{
        background-color: {COLORS['gray_50']};
    }}

    QLabel {{
        color: {COLORS['gray_900']};
        font-size: {TYPOGRAPHY['font_size_base']};
        font-weight: {TYPOGRAPHY['font_weight_normal']};
    }}

    QLabel#titleLabel {{
        font-size: {TYPOGRAPHY['font_size_2xl']};
        font-weight: {TYPOGRAPHY['font_weight_bold']};
        color: {COLORS['dark']};
        padding: {SPACING['sm']} 0px;
    }}

    QLabel#subtitleLabel {{
        font-size: {TYPOGRAPHY['font_size_lg']};
        color: {COLORS['gray_700']};
        padding: {SPACING['xs']} 0px;
    }}

    QLabel#metricLabel {{
        font-size: {TYPOGRAPHY['font_size_3xl']};
        font-weight: {TYPOGRAPHY['font_weight_bold']};
        color: {COLORS['primary']};
        padding: {SPACING['sm']};
    }}

    QLabel#statusOk {{
        background-color: {COLORS['secondary_light']};
        color: {COLORS['secondary']};
        border-radius: {BORDERS['radius_full']};
        padding: 4px 12px;
        font-weight: {TYPOGRAPHY['font_weight_semibold']};
    }}

    QLabel#statusAlert {{
        background-color: {COLORS['danger_light']};
        color: {COLORS['danger']};
        border-radius: {BORDERS['radius_full']};
        padding: 4px 12px;
        font-weight: {TYPOGRAPHY['font_weight_semibold']};
    }}

    QLabel#statusWarning {{
        background-color: {COLORS['warning_light']};
        color: {COLORS['warning']};
        border-radius: {BORDERS['radius_full']};
        padding: 4px 12px;
        font-weight: {TYPOGRAPHY['font_weight_semibold']};
    }}

    QLineEdit {{
        background-color: {COLORS['white']};
        border: {BORDERS['width_normal']} solid {COLORS['gray_300']};
        border-radius: {BORDERS['radius_md']};
        padding: 10px 14px;
        color: {COLORS['gray_900']};
        font-size: {TYPOGRAPHY['font_size_base']};
        selection-background-color: {COLORS['primary_light']};
    }}

    QLineEdit:focus {{
        border-color: {COLORS['primary']};
        background-color: {COLORS['white']};
    }}

    QLineEdit:hover {{
        border-color: {COLORS['gray_500']};
    }}

    QLineEdit::placeholder {{
        color: {COLORS['gray_500']};
        font-style: italic;
    }}

    QComboBox {{
        background-color: {COLORS['white']};
        border: {BORDERS['width_normal']} solid {COLORS['gray_300']};
        border-radius: {BORDERS['radius_md']};
        padding: 10px 14px;
        color: {COLORS['gray_900']};
        font-size: {TYPOGRAPHY['font_size_base']};
        min-width: 150px;
    }}

    QComboBox:hover {{
        border-color: {COLORS['gray_500']};
    }}

    QComboBox:focus {{
        border-color: {COLORS['primary']};
    }}

    QComboBox::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 30px;
        border-left: {BORDERS['width_thin']} solid {COLORS['gray_300']};
        border-top-right-radius: {BORDERS['radius_md']};
        border-bottom-right-radius: {BORDERS['radius_md']};
        background-color: {COLORS['gray_50']};
    }}

    QComboBox QAbstractItemView {{
        background-color: {COLORS['white']};
        border: {BORDERS['width_normal']} solid {COLORS['gray_300']};
        border-radius: {BORDERS['radius_md']};
        selection-background-color: {COLORS['primary_light']};
        selection-color: {COLORS['primary_dark']};
        padding: 4px;
    }}

    QSpinBox, QDoubleSpinBox {{
        background-color: {COLORS['white']};
        border: {BORDERS['width_normal']} solid {COLORS['gray_300']};
        border-radius: {BORDERS['radius_md']};
        padding: 10px 14px;
        color: {COLORS['gray_900']};
        font-size: {TYPOGRAPHY['font_size_base']};
    }}

    QSpinBox:focus, QDoubleSpinBox:focus {{
        border-color: {COLORS['primary']};
    }}

    QPushButton {{
        background-color: {COLORS['primary']};
        color: {COLORS['dark']};
        border: none;
        border-radius: {BORDERS['radius_md']};
        padding: 10px 20px;
        font-weight: {TYPOGRAPHY['font_weight_semibold']};
        font-size: {TYPOGRAPHY['font_size_base']};
        min-height: 20px;
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

    QPushButton#dangerBtn {{
        background-color: {COLORS['danger']};
    }}

    QPushButton#dangerBtn:hover {{
        background-color: #b91c1c;
    }}

    QPushButton#successBtn {{
        background-color: {COLORS['secondary']};
    }}

    QPushButton#successBtn:hover {{
        background-color: #047857;
    }}

    QPushButton#secondaryBtn {{
        background-color: {COLORS['white']};
        color: {COLORS['gray_700']};
        border: {BORDERS['width_normal']} solid {COLORS['gray_300']};
    }}

    QPushButton#secondaryBtn:hover {{
        background-color: {COLORS['gray_50']};
        border-color: {COLORS['gray_500']};
    }}

    QPushButton#cancelBtn {{
        background-color: {COLORS['white']};
        color: {COLORS['gray_700']};
        border: {BORDERS['width_normal']} solid {COLORS['gray_300']};
    }}

    QPushButton#cancelBtn:hover {{
        background-color: {COLORS['gray_50']};
        border-color: {COLORS['gray_500']};
    }}

    QTableWidget {{
        background-color: {COLORS['white']};
        border: {BORDERS['width_normal']} solid {COLORS['gray_300']};
        border-radius: {BORDERS['radius_lg']};
        gridline-color: {COLORS['gray_100']};
        selection-background-color: {COLORS['primary_light']};
        selection-color: {COLORS['gray_900']};
    }}

    QTableWidget::item {{
        padding: 10px 14px;
        border-bottom: {BORDERS['width_thin']} solid {COLORS['gray_100']};
    }}

    QTableWidget::item:selected {{
        background-color: {COLORS['primary_light']};
        color: {COLORS['gray_900']};
    }}

    QHeaderView::section {{
        background-color: {COLORS['gray_50']};
        color: {COLORS['gray_700']};
        padding: 12px 14px;
        border: none;
        border-bottom: {BORDERS['width_thick']} solid {COLORS['gray_300']};
        font-weight: {TYPOGRAPHY['font_weight_semibold']};
        font-size: {TYPOGRAPHY['font_size_sm']};
        text-transform: uppercase;
    }}

    QTabWidget::pane {{
        border: none;
        border-radius: {BORDERS['radius_lg']};
        background-color: {COLORS['white']};
        margin-top: -1px;
    }}

    QTabBar::tab {{
        background-color: {COLORS['gray_100']};
        color: {COLORS['gray_700']};
        padding: 12px 24px;
        margin-right: 4px;
        border-top-left-radius: {BORDERS['radius_md']};
        border-top-right-radius: {BORDERS['radius_md']};
        font-weight: {TYPOGRAPHY['font_weight_medium']};
        font-size: {TYPOGRAPHY['font_size_base']};
        min-width: 120px;
    }}

    QTabBar::tab:selected {{
        background-color: {COLORS['white']};
        color: {COLORS['primary']};
        font-weight: {TYPOGRAPHY['font_weight_semibold']};
        border-bottom: 2px solid {COLORS['primary']};
    }}

    QTabBar::tab:hover:!selected {{
        background-color: {COLORS['gray_50']};
        color: {COLORS['gray_900']};
    }}

    QCheckBox {{
        spacing: 8px;
        color: {COLORS['gray_700']};
        font-size: {TYPOGRAPHY['font_size_base']};
    }}

    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
        border-radius: {BORDERS['radius_sm']};
        border: {BORDERS['width_thick']} solid {COLORS['gray_300']};
        background-color: {COLORS['white']};
    }}

    QCheckBox::indicator:checked {{
        background-color: {COLORS['primary']};
        border-color: {COLORS['primary']};
    }}

    QScrollBar:vertical {{
        background-color: {COLORS['gray_50']};
        width: 10px;
        border-radius: 5px;
    }}

    QScrollBar::handle:vertical {{
        background-color: {COLORS['gray_300']};
        border-radius: 5px;
        min-height: 30px;
    }}

    QScrollBar::handle:vertical:hover {{
        background-color: {COLORS['gray_500']};
    }}

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}

    QMenuBar {{
        background-color: {COLORS['white']};
        color: {COLORS['gray_700']};
        border-bottom: {BORDERS['width_thin']} solid {COLORS['gray_100']};
        padding: 4px;
    }}

    QMenuBar::item {{
        padding: 8px 16px;
        border-radius: {BORDERS['radius_sm']};
    }}

    QMenuBar::item:selected {{
        background-color: {COLORS['primary_light']};
        color: {COLORS['primary']};
    }}

    QMenu {{
        background-color: {COLORS['white']};
        border: {BORDERS['width_normal']} solid {COLORS['gray_100']};
        border-radius: {BORDERS['radius_md']};
        padding: 8px;
    }}

    QMenu::item {{
        padding: 8px 32px 8px 16px;
        border-radius: {BORDERS['radius_sm']};
    }}

    QMenu::item:selected {{
        background-color: {COLORS['primary_light']};
        color: {COLORS['primary']};
    }}

    QToolTip {{
        background-color: {COLORS['gray_900']};
        color: {COLORS['white']};
        border: none;
        border-radius: {BORDERS['radius_sm']};
        padding: 8px 12px;
        font-size: {TYPOGRAPHY['font_size_sm']};
    }}

    QMessageBox {{
        background-color: {COLORS['white']};
    }}

    QMessageBox QLabel {{
        color: {COLORS['gray_900']};
        font-size: {TYPOGRAPHY['font_size_base']};
        min-width: 300px;
    }}

    QMessageBox QPushButton {{
        min-width: 100px;
        padding: 8px 16px;
    }}
    """