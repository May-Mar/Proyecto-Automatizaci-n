# Prototipo Funcional — Extractor y Validador de Facturas PDF

Este repositorio contiene un prototipo funcional (PoC) desarrollado de forma autónoma en Python para procesar, extraer y validar datos de documentos PDF de manera local.

El sistema genera de forma programática una factura de prueba en PDF y posteriormente lee el documento para extraer sus campos clave (proveedor, número de factura, fecha, montos e impuestos) y realizar validaciones aritméticas simples de control de calidad.

---

## Estructura del Proyecto

* `main.py`: Script principal que lee el archivo PDF, extrae la información a través de patrones de texto y aplica las reglas de validación de negocio.
* `crear_demo.py`: Script auxiliar para la generación local del archivo PDF simulado (`factura.pdf`).
* `requirements.txt`: Archivo de configuración que contiene las dependencias del proyecto.

---

## Tecnologías Utilizadas

* **Python 3**: Para la lógica de ejecución del backend.
* **pypdf**: Librería elegida para la lectura y extracción de texto desde archivos PDF de manera local y aislada.
* **reportlab**: Utilizada únicamente para la generación automática de la factura de prueba.

---

## Instrucciones de Ejecución

Sigue estos pasos en tu terminal para ejecutar el prototipo de forma local:

1. **Instalar las dependencias del proyecto:**
   ```bash
   pip install -r requirements.txt