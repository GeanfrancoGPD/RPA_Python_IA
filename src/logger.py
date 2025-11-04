"""
Módulo de logging
Configura el sistema de registro de eventos y errores
"""

import logging
import os
from datetime import datetime


def setup_logger(name='RPA', log_dir='logs'):
    """
    Configura y retorna un logger
    
    Args:
        name (str): Nombre del logger
        log_dir (str): Directorio para guardar logs
        
    Returns:
        logging.Logger: Logger configurado
    """
    # Crear directorio de logs si no existe
    os.makedirs(log_dir, exist_ok=True)
    
    # Crear logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Evitar duplicación de handlers
    if logger.handlers:
        return logger
    
    # Formato de los mensajes
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler para archivo
    timestamp = datetime.now().strftime("%Y%m%d")
    log_file = os.path.join(log_dir, f'rpa_{timestamp}.log')
    
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger