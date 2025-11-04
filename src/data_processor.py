"""
Módulo de procesamiento de datos (versión robusta)
Adaptado para mapear automáticamente nombres reales de columnas (ej: "Precio Venta Real",
"Precio Venta sin IGV", "Ubicación", etc.) a nombres canónicos que usa la lógica de
análisis. Evita KeyError cuando las columnas vienen con variantes en mayúsculas/espacios/tildes.
"""

import pandas as pd
import numpy as np
import unicodedata
from src.logger import setup_logger

logger = setup_logger()


class DataProcessor:
    """
    Clase que procesa y analiza datos de ventas (versión tolerante a nombres de columna)

    Cambios principales:
    - Normaliza y mapea nombres de columna (quita tildes, lower, strip)
    - Busca variantes comunes y las renombra a nombres canónicos usados internamente
    - Evita KeyError al eliminar filas nulas: usa la columna de precio detectada
    - Convierte columnas numéricas con pd.to_numeric(..., errors='coerce') antes de operar
    """

    # Nombres "canónicos" que usará internamente el procesador
    CANONICAL_COLS = {
        'Precio de venta': ['precio de venta', 'precio venta real', 'precio_venta', 'precio venta', 'precio venta (con igv)'],
        'Precio sin IGV': ['precio sin igv', 'precio venta sin igv', 'precio_venta_sin_igv', 'precio venta (sin igv)'],
        'Sede': ['sede', 'ubicación', 'ubicacion', 'ubicacion sede'],
        'Cliente': ['cliente', 'clientes'],
        'Modelo': ['modelo', 'id_vehículo', 'id_vehiculo', 'id_vehiculo', 'id_vehículo'],
        'Canal': ['canal'],
        # agregue más mapeos si hace falta
    }

    def __init__(self, excel_file):
        """
        Inicializa el procesador

        Args:
            excel_file (str): Ruta al archivo Excel con los datos
        """
        self.excel_file = excel_file
        self.df = None  # DataFrame de pandas
        self.IGV_RATE = 0.18  # Tasa de IGV del 18%
        # Columnas canónicas detectadas (después de load_data)
        self.col_price = None  # Nombre canónico para "Precio de venta"
        self.col_price_sin_igv = None  # Nombre canónico para "Precio sin IGV"

    # -----------------------------
    # UTILIDADES DE NORMALIZACIÓN
    # -----------------------------
    @staticmethod
    def _strip_accents(text: str) -> str:
        """Quita tildes/acentos y normaliza el texto"""
        if not isinstance(text, str):
            return text
        text = unicodedata.normalize('NFKD', text)
        text = ''.join([c for c in text if not unicodedata.combining(c)])
        return text

    @classmethod
    def _normalize(cls, text: str) -> str:
        """Lowercase, strip, quitar acentos y normalizar espacios/underscores"""
        if not isinstance(text, str):
            return text
        text = cls._strip_accents(text)
        text = text.strip().lower()
        text = text.replace('_', ' ')
        # collapse multiple spaces
        text = ' '.join(text.split())
        return text

    def _map_columns(self):
        """Mapea las columnas reales del DataFrame a nombres canónicos definidos.

        Renombra las columnas del DataFrame *en sitio* para que el resto del código
        pueda usar nombres estables (p. ej. 'Precio de venta', 'Precio sin IGV', 'Sede', ...).
        """
        if self.df is None:
            return

        # Construir diccionario de normalización a nombre real
        normalized_to_real = {self._normalize(col): col for col in self.df.columns}

        rename_map = {}
        # Para cada canónico, busco una variante en las columnas del excel
        for canonical, variants in self.CANONICAL_COLS.items():
            found = None
            # primero pruebo variantes explícitas definidas
            for v in variants:
                v_norm = self._normalize(v)
                if v_norm in normalized_to_real:
                    found = normalized_to_real[v_norm]
                    break
            # si no, pruebo con el nombre canónico normalizado directamente
            if found is None:
                if self._normalize(canonical) in normalized_to_real:
                    found = normalized_to_real[self._normalize(canonical)]

            if found:
                rename_map[found] = canonical
                logger.info(f"Mapeada columna: '{found}' -> '{canonical}'")
            else:
                logger.debug(f"No se encontró columna para '{canonical}' (buscando variantes: {variants})")

        if rename_map:
            self.df = self.df.rename(columns=rename_map)

        # Registrar qué columnas tenemos detectadas
        if 'Precio de venta' in self.df.columns:
            self.col_price = 'Precio de venta'
        elif 'Precio Venta Real' in self.df.columns:
            # caso raro si el renombrado no se aplicó
            self.col_price = 'Precio Venta Real'

        if 'Precio sin IGV' in self.df.columns:
            self.col_price_sin_igv = 'Precio sin IGV'
        elif 'Precio Venta sin IGV' in self.df.columns:
            self.col_price_sin_igv = 'Precio Venta sin IGV'

    # -----------------------------
    # CARGA y LIMPIEZA
    # -----------------------------
    def load_data(self):
        """
        Carga los datos desde el archivo Excel y realiza mapeo/limpieza inicial
        """
        try:
            logger.info(f"Cargando datos desde: {self.excel_file}")

            self.df = pd.read_excel(self.excel_file)

            logger.info(f"✓ Datos cargados: {len(self.df)} registros")
            logger.info(f"Columnas: {', '.join(self.df.columns.tolist())}")

            # Mapear nombres de columnas variantes a nombres canónicos
            self._map_columns()

            # Normalizar y convertir columnas numéricas que usaremos
            # Convertir precios a numérico (por si vienen como texto con comas o símbolos)
            if self.col_price in self.df.columns:
                self.df[self.col_price] = pd.to_numeric(self.df[self.col_price], errors='coerce')
            # posible columna de precio sin IGV
            if self.col_price_sin_igv in self.df.columns:
                self.df[self.col_price_sin_igv] = pd.to_numeric(self.df[self.col_price_sin_igv], errors='coerce')

            # Realizar limpieza básica de datos
            self._clean_data()

        except Exception as e:
            logger.error(f"Error al cargar datos: {str(e)}")
            raise

    def _clean_data(self):
        """
        Limpia y prepara los datos para análisis

        - Elimina filas con valores nulos en la columna de precio detectada
        - Calcula 'Precio sin IGV' si no existe (a partir de la columna de precio con IGV)
        """
        if self.df is None:
            raise ValueError("DataFrame no cargado. Ejecuta load_data() primero.")

        initial_rows = len(self.df)

        # Determinar columna precio que existe (prioridad: Precio de venta canonica)
        precio_col = None
        if self.col_price and self.col_price in self.df.columns:
            precio_col = self.col_price
        elif 'Precio Venta Real' in self.df.columns:
            precio_col = 'Precio Venta Real'
        elif 'Precio Venta' in self.df.columns:
            precio_col = 'Precio Venta'
        # también aceptar 'Precio venta real' u otras variantes si no fueron renombradas
        else:
            # buscar alguna columna cuyo nombre normalizado contenga 'precio' y 'venta'
            for c in self.df.columns:
                norm = self._normalize(c)
                if 'precio' in norm and 'venta' in norm:
                    precio_col = c
                    logger.info(f"Se asumió columna de precio: '{c}'")
                    break

        if precio_col is None:
            raise KeyError(["Precio de venta"])  # mantener compatibilidad con el error original

        # Eliminar filas donde el precio detectado sea nulo
        self.df = self.df.dropna(subset=[precio_col])

        if len(self.df) < initial_rows:
            logger.warning(f"Se eliminaron {initial_rows - len(self.df)} filas con valores nulos en '{precio_col}'")

        # Si no existe columna 'Precio sin IGV', la calculamos a partir del precio con IGV
        # Usaremos la columna canónica si fue detectada/renombrada
        if 'Precio sin IGV' not in self.df.columns and precio_col is not None:
            # asegurarse de que el precio sea numérico
            self.df[precio_col] = pd.to_numeric(self.df[precio_col], errors='coerce')
            self.df['Precio sin IGV'] = self.df[precio_col] / (1 + self.IGV_RATE)
            self.col_price_sin_igv = 'Precio sin IGV'
            logger.info("✓ Columna 'Precio sin IGV' calculada")

    # -----------------------------
    # ANÁLISIS
    # -----------------------------
    def analyze_data(self):
        logger.info("Iniciando análisis de datos...")

        results = {
            'ventas_por_sede': self._ventas_por_sede(),
            'top_modelos': self._top_modelos_vendidos(),
            'canales_ventas': self._canales_mas_ventas(),
            'segmento_clientes': self._segmento_clientes(),
            'clientes_unicos': self._contar_clientes_unicos(),
            'total_ventas': self._contar_ventas(),
            'monto_total_con_igv': self._calcular_total_con_igv(),
            'monto_total_sin_igv': self._calcular_total_sin_igv()
        }

        logger.info("✓ Análisis completado")
        return results

    # ========================================
    # ANÁLISIS INDIVIDUALES (mismos nombres canónicos)
    # ========================================

    def _ventas_por_sede(self):
        if 'Sede' in self.df.columns and 'Precio sin IGV' in self.df.columns:
            ventas = self.df.groupby('Sede')['Precio sin IGV'].sum().sort_values(ascending=False)
            logger.info(f"✓ Ventas por sede calculadas: {len(ventas)} sedes")
            return ventas
        return pd.Series(dtype=float)

    def _top_modelos_vendidos(self, top_n=5):
        # Si no hay columna 'Modelo' tratamos de detectar alguna columna que represente el modelo
        model_col = 'Modelo' if 'Modelo' in self.df.columns else None
        if model_col is None:
            # intentar columnas que contengan 'modelo' o 'vehiculo' en su nombre
            for c in self.df.columns:
                if 'modelo' in self._normalize(c) or 'vehicul' in self._normalize(c):
                    model_col = c
                    logger.info(f"Usando '{c}' como columna de modelo")
                    break

        if model_col and model_col in self.df.columns:
            top_modelos = self.df[model_col].value_counts().head(top_n)
            logger.info(f"✓ Top {top_n} modelos identificados")
            return top_modelos
        return pd.Series(dtype=int)

    def _canales_mas_ventas(self):
        if 'Canal' in self.df.columns and 'Precio sin IGV' in self.df.columns:
            canales = self.df.groupby('Canal')['Precio sin IGV'].sum().sort_values(ascending=False)
            logger.info(f"✓ Ventas por canal calculadas: {len(canales)} canales")
            return canales
        return pd.Series(dtype=float)

    def _segmento_clientes(self):
        if 'Precio sin IGV' not in self.df.columns:
            return pd.Series(dtype=int)

        precios = pd.to_numeric(self.df['Precio sin IGV'], errors='coerce').dropna()
        if precios.empty:
            return pd.Series(dtype=int)

        bins = [0, precios.quantile(0.25), precios.quantile(0.5), precios.quantile(0.75), precios.max()]
        labels = ['Bajo', 'Medio-Bajo', 'Medio-Alto', 'Alto']
        self.df['Segmento'] = pd.cut(precios.reindex(self.df.index), bins=bins, labels=labels, include_lowest=True)
        segmentos = self.df['Segmento'].value_counts()
        logger.info(f"✓ Segmentación de clientes realizada")
        return segmentos

    def _contar_clientes_unicos(self):
        if 'Cliente' in self.df.columns:
            count = self.df['Cliente'].nunique()
            logger.info(f"✓ Clientes únicos: {count}")
            return count
        return 0

    def _contar_ventas(self):
        count = len(self.df)
        logger.info(f"✓ Total de ventas: {count}")
        return count

    def _calcular_total_con_igv(self):
        if self.col_price and self.col_price in self.df.columns:
            total = pd.to_numeric(self.df[self.col_price], errors='coerce').sum()
            logger.info(f"✓ Total con IGV: ${total:,.2f}")
            return total
        # intentar otras columnas que contengan 'precio' y 'venta'
        for c in self.df.columns:
            if 'precio' in self._normalize(c) and 'venta' in self._normalize(c):
                total = pd.to_numeric(self.df[c], errors='coerce').sum()
                logger.info(f"✓ (Fallback) Total con IGV usando columna '{c}': ${total:,.2f}")
                return total
        return 0

    def _calcular_total_sin_igv(self):
        if 'Precio sin IGV' in self.df.columns:
            total = pd.to_numeric(self.df['Precio sin IGV'], errors='coerce').sum()
            logger.info(f"✓ Total sin IGV: ${total:,.2f}")
            return total
        return 0

    # ========================================
    # GENERACIÓN DE RESUMEN
    # ========================================
    def get_summary_text(self, results):
        summary = "📊 *REPORTE DE VENTAS - ANÁLISIS AUTOMÁTICO*\n"
        summary += "=" * 45 + "\n\n"
        summary += "📈 *MÉTRICAS PRINCIPALES*\n"
        summary += f"• Total de ventas: {results['total_ventas']}\n"
        summary += f"• Clientes únicos: {results['clientes_unicos']}\n"
        summary += f"• Monto total (con IGV): ${results['monto_total_con_igv']:,.2f}\n"
        summary += f"• Monto total (sin IGV): ${results['monto_total_sin_igv']:,.2f}\n\n"

        if not results['top_modelos'].empty:
            summary += "🚗 *TOP 5 MODELOS MÁS VENDIDOS*\n"
            for i, (modelo, cantidad) in enumerate(results['top_modelos'].items(), 1):
                summary += f"{i}. {modelo}: {cantidad} unidades\n"
            summary += "\n"

        if not results['ventas_por_sede'].empty:
            summary += "🏢 *VENTAS POR SEDE (sin IGV)*\n"
            for sede, monto in results['ventas_por_sede'].head(3).items():
                summary += f"• {sede}: ${monto:,.2f}\n"
            summary += "\n"

        summary += "📱 Gráficos adjuntos en los siguientes mensajes.\n"
        summary += "🤖 Reporte generado automáticamente por RPA"

        return summary
