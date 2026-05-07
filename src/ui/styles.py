"""PyQt6 Styles and Themes"""

DARK_STYLESHEET = """
    QMainWindow {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    
    QWidget {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    
    QLabel {
        color: #ffffff;
    }
    
    QPushButton {
        background-color: #0078d4;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        font-weight: bold;
        font-size: 11px;
    }
    
    QPushButton:hover {
        background-color: #106ebe;
    }
    
    QPushButton:pressed {
        background-color: #005a9e;
    }
    
    QPushButton:disabled {
        background-color: #666666;
        color: #999999;
    }
    
    QSlider::groove:horizontal {
        background-color: #444444;
        height: 8px;
        border-radius: 4px;
    }
    
    QSlider::handle:horizontal {
        background-color: #0078d4;
        width: 16px;
        margin: -4px 0;
        border-radius: 8px;
    }
    
    QSlider::handle:horizontal:hover {
        background-color: #106ebe;
    }
    
    QLineEdit {
        background-color: #333333;
        color: #ffffff;
        border: 1px solid #555555;
        border-radius: 4px;
        padding: 6px;
    }
    
    QLineEdit:focus {
        border: 2px solid #0078d4;
    }
    
    QTextEdit {
        background-color: #333333;
        color: #ffffff;
        border: 1px solid #555555;
        border-radius: 4px;
        padding: 6px;
    }
    
    QTextEdit:focus {
        border: 2px solid #0078d4;
    }
    
    QComboBox {
        background-color: #333333;
        color: #ffffff;
        border: 1px solid #555555;
        border-radius: 4px;
        padding: 6px;
    }
    
    QComboBox:focus {
        border: 2px solid #0078d4;
    }
    
    QComboBox QAbstractItemView {
        background-color: #333333;
        color: #ffffff;
        selection-background-color: #0078d4;
    }
    
    QScrollBar:vertical {
        background-color: #1e1e1e;
        width: 12px;
    }
    
    QScrollBar::handle:vertical {
        background-color: #555555;
        border-radius: 6px;
        min-height: 20px;
    }
    
    QScrollBar::handle:vertical:hover {
        background-color: #777777;
    }
    
    QScrollBar:horizontal {
        background-color: #1e1e1e;
        height: 12px;
    }
    
    QScrollBar::handle:horizontal {
        background-color: #555555;
        border-radius: 6px;
        min-width: 20px;
    }
    
    QScrollBar::handle:horizontal:hover {
        background-color: #777777;
    }
    
    QGroupBox {
        color: #ffffff;
        border: 1px solid #555555;
        border-radius: 4px;
        margin-top: 12px;
        padding-top: 12px;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 3px 0 3px;
    }
    
    QSpinBox {
        background-color: #333333;
        color: #ffffff;
        border: 1px solid #555555;
        border-radius: 4px;
        padding: 6px;
    }
    
    QSpinBox:focus {
        border: 2px solid #0078d4;
    }
    
    QDoubleSpinBox {
        background-color: #333333;
        color: #ffffff;
        border: 1px solid #555555;
        border-radius: 4px;
        padding: 6px;
    }
    
    QDoubleSpinBox:focus {
        border: 2px solid #0078d4;
    }
"""

LIGHT_STYLESHEET = """
    QMainWindow {
        background-color: #ffffff;
        color: #000000;
    }
    
    QWidget {
        background-color: #f5f5f5;
        color: #000000;
    }
    
    QLabel {
        color: #000000;
    }
    
    QPushButton {
        background-color: #0078d4;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        font-weight: bold;
        font-size: 11px;
    }
    
    QPushButton:hover {
        background-color: #106ebe;
    }
    
    QPushButton:pressed {
        background-color: #005a9e;
    }
    
    QPushButton:disabled {
        background-color: #cccccc;
        color: #999999;
    }
"""

def get_stylesheet(theme="dark"):
    """Get stylesheet for theme"""
    if theme.lower() == "light":
        return LIGHT_STYLESHEET
    return DARK_STYLESHEET
