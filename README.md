# 🤖 RPA - Sistema de Análisis de Ventas

Sistema de automatización robótica de procesos (RPA) para análisis de datos de ventas de vehículos y generación automática de reportes.

**Autor:** Basado en proyecto de Eli Mora  
**Universidad:** Rafael Urdaneta  
**Curso:** Inteligencia Artificial (Computación)

---

## 🎯 ¿Qué hace este RPA?

Este sistema automatiza completamente el proceso de análisis de ventas:

1. **Lee** un archivo Excel con datos de ventas
2. **Analiza** los datos (ventas por sede, top modelos, canales, etc.)
3. **Genera** 5 gráficos profesionales en alta resolución
4. **Envía** reportes automáticamente a WhatsApp (opcional)
5. **Registra** todo el proceso en logs detallados

---

## ✨ Características Principales

### 📊 8 Análisis Automatizados
- ✅ Ventas sin IGV por sede
- ✅ Top 5 modelos más vendidos
- ✅ Canales con más ventas
- ✅ Segmentación de clientes por precio
- ✅ Conteo de clientes únicos
- ✅ Total de ventas
- ✅ Monto total con IGV
- ✅ Monto total sin IGV

### 📈 5 Reportes Visuales
1. Gráfico de barras: Ventas por sede
2. Gráfico horizontal: Top 5 modelos
3. Gráfico de barras: Canales de venta
4. Gráfico circular: Segmentación de clientes
5. Dashboard integrado con todas las métricas

### 🤖 Automatización Completa
- Procesamiento automático de Excel
- Cálculo automático de IGV
- Generación automática de gráficos
- Envío automático a WhatsApp
- Logs detallados de cada operación

---

## 🚀 Instalación Rápida (3 pasos)

### 1. Instalar Python
Descarga Python 3.8+ desde [python.org](https://www.python.org/downloads/)

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Colocar archivo de datos
Pon tu archivo `Ventas Fundamentos.xlsx` en la carpeta `data/`

¡Listo! Ya puedes ejecutar el RPA.

---

## ▶️ Cómo Usar

### Ejecución Básica
```bash
python main.py
```

Eso es todo. El sistema hace el resto automáticamente.

### Verificar que todo funciona
```bash
python test_connection.py
```

### Ver los resultados
Los gráficos se guardan en la carpeta `output/`

---

## 📁 Estructura del Proyecto

```
rpa-ventas/
│
├── main.py                    # ⭐ EJECUTA ESTO
├── requirements.txt           # Dependencias
├── test_connection.py         # Verifica instalación
│
├── src/                       # Código fuente
│   ├── config.py              # Configuración
│   ├── logger.py              # Sistema de logs
│   ├── data_processor.py      # Análisis de datos
│   ├── report_generator.py    # Generación de gráficos
│   └── whatsapp_sender.py     # Envío a WhatsApp
│
├── data/
│   └── Ventas Fundamentos.xlsx  # 👈 PON TU EXCEL AQUÍ
│
├── output/                    # 📊 Gráficos generados aquí
└── logs/                      # 📝 Logs del sistema
```

---

## 📊 Ejemplo de Salida

Después de ejecutar `python main.py`:

```
============================================================
INICIO DEL PROCESO RPA
============================================================

Cargando configuración...
Procesando datos de ventas...
✓ Datos cargados: 179 registros

Iniciando análisis de datos...
✓ Ventas por sede calculadas: 5 sedes
✓ Top 5 modelos identificados
✓ Clientes únicos: 125
✓ Total con IGV: $5,847,234.56

Generando reportes visuales...
✓ Se generaron 5 reportes visuales

============================================================
PROCESO COMPLETADO EXITOSAMENTE
============================================================
```

---

## ⚙️ Configuración de WhatsApp (Opcional)

Si quieres recibir reportes por WhatsApp:

### 1. Crear cuenta Twilio
- Regístrate gratis en [twilio.com/try-twilio](https://www.twilio.com/try-twilio)
- Obtén tu Account SID y Auth Token

### 2. Configurar archivo .env
```bash
cp .env.example .env
```

Edita `.env`:
```env
TWILIO_ACCOUNT_SID=tu_account_sid
TWILIO_AUTH_TOKEN=tu_auth_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
WHATSAPP_TO=whatsapp:+34612345678
```

### 3. Activar WhatsApp Sandbox
- En Twilio Console: Messaging → Try it out
- Envía mensaje de activación desde tu WhatsApp

**Nota:** Sin WhatsApp configurado, el RPA funciona igual y guarda todos los reportes localmente.

---

## 🔧 Requisitos del Sistema

### Software Necesario
- Python 3.8 o superior
- pip (instalador de paquetes)

### Librerías Python
- pandas (análisis de datos)
- numpy (operaciones numéricas)
- openpyxl (lectura de Excel)
- matplotlib (gráficos)
- seaborn (estilos visuales)
- twilio (WhatsApp)
- python-dotenv (variables de entorno)

Todas se instalan con: `pip install -r requirements.txt`

---
## ❓ Problemas Comunes

### "No se encuentra el archivo Excel"
**Solución:** Coloca `Ventas Fundamentos.xlsx` en la carpeta `data/`

### "No module named 'pandas'"
**Solución:** 
```bash
pip install -r requirements.txt
```

### "Twilio authentication failed"
**Solución:** 
- Verifica credenciales en `.env`
- O deja el `.env` vacío para deshabilitar WhatsApp

### Los gráficos no se ven
**Solución:**
```bash
pip install --upgrade matplotlib seaborn
```

---

## 🎓 Aprendizajes del Proyecto

Este RPA enseña:
- ✅ Automatización de procesos repetitivos
- ✅ Análisis de datos con Pandas
- ✅ Visualización con Matplotlib
- ✅ Integración con APIs externas
- ✅ Programación modular en Python
- ✅ Manejo de archivos Excel
- ✅ Logging y manejo de errores
- ✅ Documentación de código

---

## 📝 Requisitos del Proyecto Cumplidos

### Análisis Requeridos ✅
- [x] Precio de ventas sin IGV por sede
- [x] Modelos más vendidos (top 5)
- [x] Canales con más ventas
- [x] Segmento de clientes por precio
- [x] Clientes únicos
- [x] Cantidad de ventas
- [x] Total de ventas con y sin IGV

### Visualizaciones Requeridas ✅
- [x] Gráfico de barras: Ventas por sede
- [x] Gráfico horizontal: Top 5 modelos
- [x] Gráfico de barras: Canales
- [x] Gráfico circular: Segmentación
- [x] Dashboard resumen

### Entregables ✅
- [x] Código completo y funcional
- [x] Comentado y documentado
- [x] Organizado modularmente
- [x] Manejo de errores robusto
- [x] README.md completo
- [x] requirements.txt
- [x] .gitignore
- [x] Commits organizados (listo para GitHub)
---

## 📄 Licencia

Proyecto educativo - Universidad Rafael Urdaneta

---

**¡Listo para automatizar! 🚀**

Ejecuta: `python main.py` y observa la magia del RPA en acción.
