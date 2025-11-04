"""
Módulo de generación de reportes visuales
Responsable de: crear gráficos, visualizaciones y dashboards
"""

import os
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime
from src.logger import setup_logger

# Configurar backend de matplotlib para guardar archivos sin mostrar ventanas
matplotlib.use('Agg')

logger = setup_logger()


class ReportGenerator:
    """
    Clase para generar reportes visuales (gráficos PNG)
    
    RESPONSABILIDADES:
    - Crear gráficos de barras
    - Crear gráficos circulares
    - Crear dashboard integrado
    - Guardar imágenes en alta resolución
    """
    
    def __init__(self, output_dir):
        """
        Inicializa el generador de reportes
        
        Args:
            output_dir (str): Directorio donde guardar los gráficos
        """
        self.output_dir = output_dir
        # Timestamp para nombres únicos de archivos
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Configurar estilo visual de los gráficos
        # seaborn-v0_8-darkgrid: estilo profesional con rejilla
        plt.style.use('seaborn-v0_8-darkgrid')
        
    def generate_all_reports(self, df, analysis_results):
        """
        Genera TODOS los reportes visuales requeridos
        
        GRÁFICOS QUE GENERA:
        1. Ventas por sede (barras verticales)
        2. Top 5 modelos (barras horizontales)
        3. Canales de venta (barras verticales)
        4. Segmentación de clientes (gráfico circular)
        5. Dashboard resumen (panel integrado)
        
        Args:
            df (DataFrame): DataFrame con todos los datos
            analysis_results (dict): Resultados del análisis
            
        Returns:
            list: Lista de rutas de archivos PNG generados
        """
        report_files = []  # Aquí guardaremos las rutas de los archivos
        
        try:
            # GRÁFICO 1: Ventas por sede
            file1 = self._grafico_ventas_por_sede(analysis_results['ventas_por_sede'])
            if file1:
                report_files.append(file1)
            
            # GRÁFICO 2: Top modelos
            file2 = self._grafico_top_modelos(analysis_results['top_modelos'])
            if file2:
                report_files.append(file2)
            
            # GRÁFICO 3: Canales
            file3 = self._grafico_canales(analysis_results['canales_ventas'])
            if file3:
                report_files.append(file3)
            
            # GRÁFICO 4: Segmentación
            file4 = self._grafico_segmentacion(analysis_results['segmento_clientes'])
            if file4:
                report_files.append(file4)
            
            # GRÁFICO 5: Dashboard
            file5 = self._dashboard_resumen(analysis_results)
            if file5:
                report_files.append(file5)
            
            logger.info(f"✓ Se generaron {len(report_files)} reportes visuales")
            
        except Exception as e:
            logger.error(f"Error al generar reportes: {str(e)}")
        
        return report_files
    
    # ========================================
    # GRÁFICOS INDIVIDUALES
    # ========================================
    
    def _grafico_ventas_por_sede(self, ventas_por_sede):
        """
        GRÁFICO 1: Gráfico de barras verticales de ventas sin IGV por sede
        
        ELEMENTOS:
        - Barras verticales de color azul acero
        - Valores numéricos encima de cada barra
        - Eje X rotado 45° para mejor lectura
        
        Args:
            ventas_por_sede (Series): Datos de ventas por sede
            
        Returns:
            str: Ruta del archivo PNG generado (o None si hay error)
        """
        if ventas_por_sede.empty:
            return None
        
        try:
            # Crear figura y eje
            # figsize=(12, 6): ancho=12 pulgadas, alto=6 pulgadas
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Crear gráfico de barras
            # kind='bar': barras verticales
            # color='steelblue': azul acero
            # alpha=0.8: 80% opacidad (ligeramente transparente)
            ventas_por_sede.plot(kind='bar', ax=ax, color='steelblue', alpha=0.8)
            
            # Configurar títulos y etiquetas
            ax.set_title('Ventas sin IGV por Sede', fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Sede', fontsize=12)
            ax.set_ylabel('Ventas sin IGV ($)', fontsize=12)
            ax.tick_params(axis='x', rotation=45)  # Rotar etiquetas del eje X
            
            # Agregar valores encima de cada barra
            for i, v in enumerate(ventas_por_sede):
                # text(x, y, texto)
                # ha='center': centrado horizontal
                # va='bottom': alineado al fondo (arriba de la barra)
                ax.text(i, v, f'${v:,.0f}', ha='center', va='bottom')
            
            # tight_layout(): ajusta automáticamente el espaciado
            plt.tight_layout()
            
            # Guardar imagen
            filename = os.path.join(self.output_dir, f'ventas_por_sede_{self.timestamp}.png')
            # dpi=300: alta resolución (300 puntos por pulgada)
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()  # Cerrar figura para liberar memoria
            
            logger.info(f"✓ Gráfico de ventas por sede guardado: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error al generar gráfico de ventas por sede: {str(e)}")
            return None
    
    def _grafico_top_modelos(self, top_modelos):
        """
        GRÁFICO 2: Gráfico de barras HORIZONTALES de top modelos
        
        POR QUÉ HORIZONTAL:
        - Los nombres de modelos pueden ser largos
        - Mejor legibilidad con barras horizontales
        
        Args:
            top_modelos (Series): Datos de top 5 modelos
            
        Returns:
            str: Ruta del archivo PNG
        """
        if top_modelos.empty:
            return None
        
        try:
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # kind='barh': barras HORIZONTALES (h = horizontal)
            top_modelos.plot(kind='barh', ax=ax, color='coral', alpha=0.8)
            
            ax.set_title('Top 5 Modelos Más Vendidos', fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Cantidad de Ventas', fontsize=12)
            ax.set_ylabel('Modelo', fontsize=12)
            
            # Agregar valores al final de cada barra
            for i, v in enumerate(top_modelos):
                ax.text(v, i, f' {v}', va='center')  # Espacio antes del número
            
            plt.tight_layout()
            
            filename = os.path.join(self.output_dir, f'top_modelos_{self.timestamp}.png')
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"✓ Gráfico de top modelos guardado: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error al generar gráfico de top modelos: {str(e)}")
            return None
    
    def _grafico_canales(self, canales_ventas):
        """
        GRÁFICO 3: Gráfico de barras de canales con más ventas
        
        Args:
            canales_ventas (Series): Datos de ventas por canal
            
        Returns:
            str: Ruta del archivo PNG
        """
        if canales_ventas.empty:
            return None
        
        try:
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Color verde mar para canales
            canales_ventas.plot(kind='bar', ax=ax, color='seagreen', alpha=0.8)
            
            ax.set_title('Canales con Más Ventas', fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Canal', fontsize=12)
            ax.set_ylabel('Ventas sin IGV ($)', fontsize=12)
            ax.tick_params(axis='x', rotation=45)
            
            # Valores en las barras
            for i, v in enumerate(canales_ventas):
                ax.text(i, v, f'${v:,.0f}', ha='center', va='bottom')
            
            plt.tight_layout()
            
            filename = os.path.join(self.output_dir, f'canales_ventas_{self.timestamp}.png')
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"✓ Gráfico de canales guardado: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error al generar gráfico de canales: {str(e)}")
            return None
    
    def _grafico_segmentacion(self, segmento_clientes):
        """
        GRÁFICO 4: Gráfico circular (PIE CHART) de segmentación de clientes
        
        ELEMENTOS:
        - Colores personalizados para cada segmento
        - Porcentajes automáticos
        - Efecto "explosión" (explode) para destacar segmentos
        - Sombra para efecto 3D sutil
        
        Args:
            segmento_clientes (Series): Datos de segmentación
            
        Returns:
            str: Ruta del archivo PNG
        """
        if segmento_clientes.empty:
            return None
        
        try:
            fig, ax = plt.subplots(figsize=(10, 8))
            
            # Colores pastel para cada segmento
            colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
            
            # explode: separación de cada porción del centro
            # [0.05, 0.05, ...] = separar 0.05 unidades cada porción
            explode = [0.05] * len(segmento_clientes)
            
            # Crear gráfico circular
            # autopct='%1.1f%%': mostrar porcentajes con 1 decimal
            # startangle=90: empezar desde arriba (90 grados)
            # shadow=True: agregar sombra
            ax.pie(segmento_clientes, 
                   labels=segmento_clientes.index, 
                   autopct='%1.1f%%',
                   startangle=90, 
                   colors=colors, 
                   explode=explode, 
                   shadow=True)
            
            ax.set_title('Segmentación de Clientes por Ventas sin IGV', 
                        fontsize=16, fontweight='bold', pad=20)
            
            plt.tight_layout()
            
            filename = os.path.join(self.output_dir, f'segmentacion_clientes_{self.timestamp}.png')
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"✓ Gráfico de segmentación guardado: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error al generar gráfico de segmentación: {str(e)}")
            return None
    
    def _dashboard_resumen(self, results):
        """
        GRÁFICO 5: Dashboard integrado con TODAS las métricas clave
        
        DISEÑO:
        - Figura grande (14x10 pulgadas)
        - Grid de 3 filas x 2 columnas
        - Métricas principales en la parte superior
        - Gráficos pequeños de cada análisis abajo
        
        SUBPLOTS:
        [Métricas Principales   ]  <- Fila 0, ocupa 2 columnas
        [Top 3 Sedes][Top 3 Mod.]  <- Fila 1
        [Canales    ][Segmentos ]  <- Fila 2
        
        Args:
            results (dict): Todos los resultados del análisis
            
        Returns:
            str: Ruta del archivo PNG
        """
        try:
            # Crear figura grande
            fig = plt.figure(figsize=(14, 10))
            
            # Título principal del dashboard
            fig.suptitle('Dashboard de Ventas - Resumen Ejecutivo', 
                        fontsize=20, fontweight='bold', y=0.98)
            
            # Crear grid de subplots
            # 3 filas, 2 columnas, espaciado entre gráficos
            gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
            
            # ====================================
            # SUBPLOT 1: Métricas principales (texto)
            # ====================================
            ax1 = fig.add_subplot(gs[0, :])  # Fila 0, todas las columnas
            ax1.axis('off')  # Ocultar ejes (solo mostrar texto)
            
            # Construir texto con métricas
            metrics_text = (
                f"Total de Ventas: {results['total_ventas']:,}\n"
                f"Clientes Únicos: {results['clientes_unicos']:,}\n"
                f"Monto Total con IGV: ${results['monto_total_con_igv']:,.2f}\n"
                f"Monto Total sin IGV: ${results['monto_total_sin_igv']:,.2f}"
            )
            
            # Mostrar texto centrado con fondo
            # bbox: cuadro con fondo color trigo y esquinas redondeadas
            ax1.text(0.5, 0.5, metrics_text, 
                    ha='center', va='center', 
                    fontsize=14, 
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            
            # ====================================
            # SUBPLOT 2: Top 3 Sedes
            # ====================================
            if not results['ventas_por_sede'].empty:
                ax2 = fig.add_subplot(gs[1, 0])  # Fila 1, columna 0
                top_sedes = results['ventas_por_sede'].head(3)
                top_sedes.plot(kind='bar', ax=ax2, color='steelblue', alpha=0.7)
                ax2.set_title('Top 3 Sedes', fontweight='bold')
                ax2.set_xlabel('')
                ax2.tick_params(axis='x', rotation=45)
            
            # ====================================
            # SUBPLOT 3: Top 3 Modelos
            # ====================================
            if not results['top_modelos'].empty:
                ax3 = fig.add_subplot(gs[1, 1])  # Fila 1, columna 1
                top_3_modelos = results['top_modelos'].head(3)
                top_3_modelos.plot(kind='barh', ax=ax3, color='coral', alpha=0.7)
                ax3.set_title('Top 3 Modelos', fontweight='bold')
                ax3.set_xlabel('')
            
            # ====================================
            # SUBPLOT 4: Canales
            # ====================================
            if not results['canales_ventas'].empty:
                ax4 = fig.add_subplot(gs[2, 0])  # Fila 2, columna 0
                results['canales_ventas'].plot(kind='bar', ax=ax4, color='seagreen', alpha=0.7)
                ax4.set_title('Ventas por Canal', fontweight='bold')
                ax4.set_xlabel('')
                ax4.tick_params(axis='x', rotation=45)
            
            # ====================================
            # SUBPLOT 5: Segmentación
            # ====================================
            if not results['segmento_clientes'].empty:
                ax5 = fig.add_subplot(gs[2, 1])  # Fila 2, columna 1
                results['segmento_clientes'].plot(kind='pie', ax=ax5, autopct='%1.1f%%',
                                                 colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'])
                ax5.set_title('Segmentación de Clientes', fontweight='bold')
                ax5.set_ylabel('')  # Quitar etiqueta del eje Y
            
            # Guardar dashboard completo
            filename = os.path.join(self.output_dir, f'dashboard_resumen_{self.timestamp}.png')
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"✓ Dashboard resumen guardado: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error al generar dashboard: {str(e)}")
            return None