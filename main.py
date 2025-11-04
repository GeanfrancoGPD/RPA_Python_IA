"""
RPA - Sistema de Análisis de Ventas y Reportes Automáticos
Autor: Basado en proyecto de Eli Mora
Universidad Rafael Urdaneta

Este es el archivo PRINCIPAL que ejecuta todo el proceso del RPA.
Orquesta: carga de datos -> análisis -> reportes -> envío WhatsApp
"""

import os
import sys
from datetime import datetime
from src.data_processor import DataProcessor
from src.report_generator import ReportGenerator
from src.whatsapp_sender import WhatsAppSender
from src.config import Config
from src.logger import setup_logger

# Configurar logger (sistema de registro de eventos)
logger = setup_logger()


def main():
    """
    Función principal del RPA
    
    FLUJO DEL PROCESO:
    1. Cargar configuración (rutas, credenciales)
    2. Verificar que existe el archivo Excel
    3. Procesar y analizar los datos
    4. Generar gráficos y reportes visuales
    5. Enviar reportes a WhatsApp (si está configurado)
    6. Mostrar resumen final
    """
    try:
        # ============================================
        # INICIO DEL PROCESO
        # ============================================
        logger.info("=" * 60)
        logger.info("INICIO DEL PROCESO RPA")
        logger.info("=" * 60)
        
        # ============================================
        # PASO 1: CARGAR CONFIGURACIÓN
        # ============================================
        logger.info("Cargando configuración...")
        config = Config()
        
        # ============================================
        # PASO 2: VERIFICAR ARCHIVO DE DATOS
        # ============================================
        # Verificamos que el archivo Excel exista antes de continuar
        if not os.path.exists(config.EXCEL_FILE):
            logger.error(f"No se encuentra el archivo: {config.EXCEL_FILE}")
            logger.info("Por favor, coloca el archivo 'Ventas Fundamentos.xlsx' en la carpeta 'data/'")
            return
        
        # ============================================
        # PASO 3: PROCESAR DATOS
        # ============================================
        logger.info("Procesando datos de ventas...")
        
        # Crear procesador de datos
        processor = DataProcessor(config.EXCEL_FILE)
        
        # Cargar datos del Excel
        processor.load_data()
        
        # Realizar todos los análisis requeridos
        analysis_results = processor.analyze_data()
        
        # ============================================
        # PASO 4: GENERAR REPORTES VISUALES
        # ============================================
        logger.info("Generando reportes visuales...")
        
        # Crear generador de reportes
        report_gen = ReportGenerator(config.OUTPUT_DIR)
        
        # Generar todos los gráficos
        # Retorna lista de rutas de archivos generados
        report_files = report_gen.generate_all_reports(
            processor.df,              # DataFrame con los datos
            analysis_results           # Resultados del análisis
        )
        
        # ============================================
        # PASO 5: ENVIAR REPORTES A WHATSAPP (OPCIONAL)
        # ============================================
        if config.ENABLE_WHATSAPP:
            logger.info("Enviando reportes a WhatsApp...")
            
            # Crear cliente de WhatsApp
            whatsapp = WhatsAppSender(
                config.TWILIO_ACCOUNT_SID,
                config.TWILIO_AUTH_TOKEN,
                config.TWILIO_WHATSAPP_FROM
            )
            
            # Enviar resumen de texto
            summary_text = processor.get_summary_text(analysis_results)
            whatsapp.send_message(config.WHATSAPP_TO, summary_text)
            
            # Enviar gráficos como imágenes
            for file_path in report_files:
                whatsapp.send_image(config.WHATSAPP_TO, file_path)
            
            logger.info("✓ Reportes enviados exitosamente a WhatsApp")
        else:
            logger.info("Envío a WhatsApp deshabilitado en configuración")
        
        # ============================================
        # PASO 6: RESUMEN FINAL
        # ============================================
        logger.info("=" * 60)
        logger.info("PROCESO COMPLETADO EXITOSAMENTE")
        logger.info(f"Reportes generados en: {config.OUTPUT_DIR}")
        logger.info(f"Total de archivos: {len(report_files)}")
        logger.info("=" * 60)
        
    except Exception as e:
        # Si algo sale mal, registramos el error completo
        logger.error(f"Error en el proceso principal: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    # Este bloque solo se ejecuta cuando corres: python main.py
    # No se ejecuta si importas este archivo desde otro script
    main()