"""Custom PyQt6 Widgets"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSlider, QSpinBox, QComboBox, QFileDialog, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QFrame


class ImagePreviewWidget(QWidget):
    """Widget para preview de imagens"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Preview area
        self.preview_label = QLabel("Nenhuma imagem selecionada")
        self.preview_label.setStyleSheet(
            "border: 2px dashed #555555; padding: 20px; text-align: center; background-color: #333333;"
        )
        self.preview_label.setMinimumHeight(300)
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(QLabel("Preview:"))
        layout.addWidget(self.preview_label)
        
        self.setLayout(layout)
    
    def set_image(self, pixmap):
        """Set image to preview"""
        if pixmap:
            scaled = pixmap.scaledToHeight(300, Qt.TransformationMode.SmoothTransformation)
            self.preview_label.setPixmap(scaled)
        else:
            self.preview_label.setPixmap(QPixmap())
            self.preview_label.setText("Nenhuma imagem selecionada")


class ControlPanelWidget(QWidget):
    """Widget para controles do device"""
    
    brightness_changed = pyqtSignal(int)
    contrast_changed = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Brightness control
        bright_layout = QHBoxLayout()
        bright_layout.addWidget(QLabel("Brilho:"))
        self.brightness_slider = QSlider(Qt.Orientation.Horizontal)
        self.brightness_slider.setMinimum(0)
        self.brightness_slider.setMaximum(100)
        self.brightness_slider.setValue(50)
        self.brightness_slider.valueChanged.connect(self.brightness_changed.emit)
        self.brightness_value = QLabel("50%")
        self.brightness_slider.valueChanged.connect(
            lambda v: self.brightness_value.setText(f"{v}%")
        )
        bright_layout.addWidget(self.brightness_slider)
        bright_layout.addWidget(self.brightness_value)
        
        # Contrast control
        contrast_layout = QHBoxLayout()
        contrast_layout.addWidget(QLabel("Contraste:"))
        self.contrast_slider = QSlider(Qt.Orientation.Horizontal)
        self.contrast_slider.setMinimum(0)
        self.contrast_slider.setMaximum(100)
        self.contrast_slider.setValue(50)
        self.contrast_slider.valueChanged.connect(self.contrast_changed.emit)
        self.contrast_value = QLabel("50%")
        self.contrast_slider.valueChanged.connect(
            lambda v: self.contrast_value.setText(f"{v}%")
        )
        contrast_layout.addWidget(self.contrast_slider)
        contrast_layout.addWidget(self.contrast_value)
        
        layout.addLayout(bright_layout)
        layout.addLayout(contrast_layout)
        layout.addStretch()
        
        self.setLayout(layout)


class MediaManagerWidget(QWidget):
    """Widget para gerenciar mídia"""
    
    file_selected = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.current_file = None
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # File selection
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("Arquivo:"))
        self.file_label = QLabel("Nenhum arquivo selecionado")
        self.file_label.setStyleSheet(
            "padding: 6px; background-color: #333333; border-radius: 4px;"
        )
        file_layout.addWidget(self.file_label)
        
        self.browse_btn = QPushButton("Procurar...")
        self.browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(self.browse_btn)
        
        # Supported formats
        formats_label = QLabel("Formatos suportados: PNG, JPG, GIF, MP4, WebM")
        formats_label.setStyleSheet("color: #aaaaaa; font-size: 10px;")
        
        layout.addLayout(file_layout)
        layout.addWidget(formats_label)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def browse_file(self):
        """Open file browser"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar Arquivo",
            "",
            "Imagens e Vídeos (*.png *.jpg *.jpeg *.gif *.mp4 *.webm);;Imagens (*.png *.jpg *.jpeg *.gif);;Vídeos (*.mp4 *.webm);;Todos (*)"
        )
        
        if file_path:
            self.current_file = file_path
            file_name = file_path.split('/')[-1]
            self.file_label.setText(file_name)
            self.file_selected.emit(file_path)
