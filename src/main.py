#!/usr/bin/env python3
"""ProFlow 240 Control - Main Entry Point"""

import sys
import logging
from pathlib import Path

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from ui.main_window import MainWindow
from utils.logger import setup_logger
from utils.config import Config

# Setup logging
logger = setup_logger(__name__)

def main():
    """Main application entry point"""
    try:
        # Initialize config
        config = Config()
        logger.info(f"ProFlow 240 Control v1.0.0 iniciado")
        logger.info(f"Config path: {config.config_dir}")
        
        # Create Qt Application
        app = QApplication(sys.argv)
        app.setApplicationName("ProFlow 240 Control")
        app.setApplicationVersion("1.0.0")
        app.setStyle('Fusion')
        
        # Create Main Window
        window = MainWindow(config)
        window.show()
        
        logger.info("Interface gráfica carregada com sucesso")
        
        # Run application
        sys.exit(app.exec())
        
    except Exception as e:
        logger.error(f"Erro ao iniciar aplicação: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
