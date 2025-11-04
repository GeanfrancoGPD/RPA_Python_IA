"""
Paquete RPA - Sistema de Análisis de Ventas
Módulos principales del sistema de automatización
"""

__version__ = '1.0.0'
__author__ = 'Basado en proyecto de Eli Mora'
__university__ = 'Universidad Rafael Urdaneta'

from .config import Config
from .logger import setup_logger
from .data_processor import DataProcessor
from .report_generator import ReportGenerator
from .whatsapp_sender import WhatsAppSender

__all__ = [
    'Config',
    'setup_logger',
    'DataProcessor',
    'ReportGenerator',
    'WhatsAppSender'
]