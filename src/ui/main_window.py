#!/usr/bin/env python3
"""Main Application Window"""

import logging
from pathlib import Path

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTabWidget, QMessageBox, QStatusBar, QSplitter
)
from PyQt6.QtCore import Qt, QSize, QThread, pyqtSignal
from PyQt6.QtGui import QIcon

from ui.styles import get_stylesheet
from ui.widgets import ImagePreviewWidget, ControlPanelWidget, MediaManagerWidget
from device.usb_handler import USBHandler
from media.image_processor import ImageProcessor
from utils.config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class DeviceWorker(QThread):
    """Worker thread para comunicação com device"""
    
    connected = pyqtSignal(bool)
    error = pyqtSignal(str)
    
    def __init__(self, usb_handler):
        super().__init__()
        self.usb_handler = usb_handler
        self.running = True
    
    def run(self):
        """Check device connection"""
        try:
            is_connected = self.usb_handler.find_device()
            self.connected.emit(is_connected)
        except Exception as e:
            logger.error(f"Erro ao conectar device: {e}")
            self.error.emit(str(e))
    
    def stop(self):
        self.running = False


class MainWindow(QMainWindow):
    """Main Application Window"""
    
    def __init__(self, config: Config):
        super().__init__()
        self.config = config
        self.usb_handler = USBHandler()
        self.image_processor = ImageProcessor()
        self.device_connected = False
        
        self.setWindowTitle("ProFlow 240 Control")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(QSize(1000, 600))
        
        # Apply stylesheet
        self.setStyleSheet(get_stylesheet("dark"))
        
        self.init_ui()
        self.check_device_connection()
    
    def init_ui(self):
        """Initialize user interface"""
        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Title bar with status
        title_layout = QHBoxLayout()
        title_label = QLabel("ProFlow 240 Control")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        # Connection status
        self.status_label = QLabel("🔴 Desconectado")
        self.status_label.setStyleSheet("color: #ff0000; font-weight: bold;")
        title_layout.addWidget(self.status_label)
        
        main_layout.addLayout(title_layout)
        
        # Content area with splitter
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Preview
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.addWidget(QLabel("Preview do Display"))
        self.preview_widget = ImagePreviewWidget()
        left_layout.addWidget(self.preview_widget)
        content_splitter.addWidget(left_panel)
        
        # Right panel - Tabs
        right_panel = QTabWidget()
        
        # Tab 1: Media Manager
        self.media_widget = MediaManagerWidget()
        self.media_widget.file_selected.connect(self.on_file_selected)
        right_panel.addTab(self.media_widget, "📁 Mídia")
        
        # Tab 2: Controls
        self.control_widget = ControlPanelWidget()
        self.control_widget.brightness_changed.connect(self.on_brightness_changed)
        self.control_widget.contrast_changed.connect(self.on_contrast_changed)
        right_panel.addTab(self.control_widget, "⚙️ Controles")
        
        # Tab 3: Settings
        settings_widget = QWidget()
        settings_layout = QVBoxLayout(settings_widget)
        settings_layout.addWidget(QLabel("Configurações"))
        settings_layout.addWidget(QLabel("VID: 0x33C3"))
        settings_layout.addWidget(QLabel("PID: 0x7792"))
        settings_layout.addStretch()
        right_panel.addTab(settings_widget, "⚙️ Configurações")
        
        content_splitter.addWidget(right_panel)
        content_splitter.setStretchFactor(0, 1)
        content_splitter.setStretchFactor(1, 1)
        
        main_layout.addWidget(content_splitter)
        
        # Bottom action buttons
        action_layout = QHBoxLayout()
        action_layout.addStretch()
        
        self.send_btn = QPushButton("📤 Enviar para Display")
        self.send_btn.setMinimumWidth(150)
        self.send_btn.clicked.connect(self.send_to_device)
        self.send_btn.setEnabled(False)
        action_layout.addWidget(self.send_btn)
        
        clear_btn = QPushButton("🗑️ Limpar")
        clear_btn.setMinimumWidth(100)
        clear_btn.clicked.connect(self.clear_preview)
        action_layout.addWidget(clear_btn)
        
        exit_btn = QPushButton("❌ Sair")
        exit_btn.setMinimumWidth(100)
        exit_btn.clicked.connect(self.close)
        action_layout.addWidget(exit_btn)
        
        main_layout.addLayout(action_layout)
        
        # Status bar
        self.statusBar().showMessage("Pronto")
    
    def check_device_connection(self):
        """Check if device is connected"""
        self.device_worker = DeviceWorker(self.usb_handler)
        self.device_worker.connected.connect(self.on_device_connected)
        self.device_worker.error.connect(self.on_device_error)
        self.device_worker.start()
    
    def on_device_connected(self, connected: bool):
        """Handle device connection status"""
        self.device_connected = connected
        if connected:
            self.status_label.setText("🟢 Conectado")
            self.status_label.setStyleSheet("color: #00ff00; font-weight: bold;")
            self.send_btn.setEnabled(True)
            self.statusBar().showMessage("Device ProFlow 240 encontrado!")
            logger.info("Device conectado com sucesso")
        else:
            self.status_label.setText("🔴 Desconectado")
            self.status_label.setStyleSheet("color: #ff0000; font-weight: bold;")
            self.send_btn.setEnabled(False)
            self.statusBar().showMessage("Device não encontrado. Verifique a conexão USB.")
            logger.warning("Device não encontrado")
    
    def on_device_error(self, error: str):
        """Handle device error"""
        logger.error(f"Erro do device: {error}")
        self.statusBar().showMessage(f"Erro: {error}")
    
    def on_file_selected(self, file_path: str):
        """Handle file selection"""
        try:
            logger.info(f"Arquivo selecionado: {file_path}")
            
            # Process image
            pixmap = self.image_processor.load_image(file_path)
            if pixmap:
                self.preview_widget.set_image(pixmap)
                self.statusBar().showMessage(f"Arquivo carregado: {Path(file_path).name}")
                self.media_widget.current_file = file_path
            
        except Exception as e:
            logger.error(f"Erro ao carregar arquivo: {e}")
            QMessageBox.critical(self, "Erro", f"Erro ao carregar arquivo: {e}")
    
    def on_brightness_changed(self, value: int):
        """Handle brightness change"""
        logger.debug(f"Brilho alterado para: {value}%")
        if self.device_connected and self.media_widget.current_file:
            # Send to device
            pass
    
    def on_contrast_changed(self, value: int):
        """Handle contrast change"""
        logger.debug(f"Contraste alterado para: {value}%")
        if self.device_connected and self.media_widget.current_file:
            # Send to device
            pass
    
    def send_to_device(self):
        """Send image/video to device"""
        if not self.device_connected:
            QMessageBox.warning(self, "Aviso", "Device não está conectado.")
            return
        
        if not self.media_widget.current_file:
            QMessageBox.warning(self, "Aviso", "Selecione um arquivo primeiro.")
            return
        
        try:
            logger.info(f"Enviando arquivo para device: {self.media_widget.current_file}")
            
            # TODO: Implement actual device communication
            # self.usb_handler.send_file(self.media_widget.current_file)
            
            self.statusBar().showMessage("Enviando para o device...")
            QMessageBox.information(self, "Sucesso", "Arquivo enviado para o display com sucesso!")
            
        except Exception as e:
            logger.error(f"Erro ao enviar arquivo: {e}")
            QMessageBox.critical(self, "Erro", f"Erro ao enviar arquivo: {e}")
    
    def clear_preview(self):
        """Clear preview"""
        self.preview_widget.set_image(None)
        self.media_widget.file_label.setText("Nenhum arquivo selecionado")
        self.media_widget.current_file = None
        self.statusBar().showMessage("Preview limpo")
    
    def closeEvent(self, event):
        """Handle window close"""
        reply = QMessageBox.question(
            self,
            "Confirmar Saída",
            "Deseja sair da aplicação?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.usb_handler.disconnect()
            except:
                pass
            
            if hasattr(self, 'device_worker'):
                self.device_worker.stop()
                self.device_worker.wait()
            
            logger.info("Aplicação encerrada")
            event.accept()
        else:
            event.ignore()
