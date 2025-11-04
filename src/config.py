"""
Módulo de configuración centralizada
Gestiona todas las variables de configuración del RPA
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class Config:
    """
    Clase de configuración centralizada
    """
    
    def __init__(self):
        # Rutas de archivos
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.DATA_DIR = os.path.join(self.BASE_DIR, 'data')
        self.OUTPUT_DIR = os.path.join(self.BASE_DIR, 'output')
        self.LOGS_DIR = os.path.join(self.BASE_DIR, 'logs')
        
        # Archivo de datos
        self.EXCEL_FILE = os.path.join(self.DATA_DIR, 'Ventas_Fundamentos.xlsx')
        
        # Crear directorios si no existen
        os.makedirs(self.DATA_DIR, exist_ok=True)
        os.makedirs(self.OUTPUT_DIR, exist_ok=True)
        os.makedirs(self.LOGS_DIR, exist_ok=True)
        
        # Configuración de Twilio (WhatsApp)
        self.TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
        self.TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
        self.TWILIO_WHATSAPP_FROM = os.getenv('TWILIO_WHATSAPP_FROM', 'whatsapp:+14155238886')
        self.WHATSAPP_TO = os.getenv('WHATSAPP_TO', '')
        
        # Habilitar/deshabilitar envío a WhatsApp
        self.ENABLE_WHATSAPP = self._check_whatsapp_config()
        
        # Configuración de análisis
        self.TOP_MODELS_COUNT = 5  # Top 5 modelos más vendidos
        self.IGV_RATE = 0.18  # Tasa de IGV (18%)
        
    def _check_whatsapp_config(self):
        """
        Verifica si la configuración de WhatsApp está completa
        """
        required = [
            self.TWILIO_ACCOUNT_SID,
            self.TWILIO_AUTH_TOKEN,
            self.WHATSAPP_TO
        ]
        return all(required)
    
    def display_config(self):
        """
        Muestra la configuración actual (sin credenciales sensibles)
        """
        print("=" * 60)
        print("CONFIGURACIÓN DEL SISTEMA")
        print("=" * 60)
        print(f"Directorio base: {self.BASE_DIR}")
        print(f"Archivo de datos: {self.EXCEL_FILE}")
        print(f"Directorio de salida: {self.OUTPUT_DIR}")
        print(f"WhatsApp habilitado: {self.ENABLE_WHATSAPP}")
        print("=" * 60)