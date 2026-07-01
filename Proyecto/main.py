import os
import re
from pypdf import PdfReader

def extraer_texto_pdf(ruta_pdf):
    """Lee el PDF local y extrae todo su texto."""
    if not os.path.exists(ruta_pdf):
        print(f"Error: No se encontró el archivo '{ruta_pdf}' en la carpeta actual.")
        return None
        
    try:
        reader = PdfReader(ruta_pdf)
        texto_completo = ""
        for pagina in reader.pages:
            texto_completo += pagina.extract_text() or ""
        return texto_completo
    except Exception as e:
        print(f"Error al leer el archivo PDF: {e}")
        return None

def analizar_datos_factura(texto):
    """Busca patrones clave en el texto extraído."""
    datos = {
        "proveedor": "No detectado",
        "numero_factura": "No detectado",
        "fecha": "No detectada",
        "monto_neto": 0.0,
        "impuesto": 0.0,
        "monto_total": 0.0
    }
    
    # 1. Búsqueda simple de Proveedor (ejemplo basado en palabras clave comunes)
    if "reparaciones xl" in texto.lower():
        datos["proveedor"] = "Reparaciones XL"
    elif "amazon" in texto.lower():
        datos["proveedor"] = "Amazon Web Services"
    else:
        # Intenta tomar la primera línea no vacía como posible nombre de proveedor
        lineas = [l.strip() for l in texto.split("\n") if l.strip()]
        if lineas:
            datos["proveedor"] = lineas[0]

    # 2. Búsqueda de Número de Factura (ej. "Factura No: 123", "Ref: ABC-12")
    match_numero = re.search(r'(?:factura|bill|invoice|n[o°]|ref)[:\s\-]*([A-Za-z0-9\-]+)', texto, re.IGNORECASE)
    if match_numero:
        datos["numero_factura"] = match_numero.group(1)
        
    # 3. Búsqueda de Fecha (Formatos: DD/MM/AAAA, DD-MM-AAAA, AAAA-MM-DD)
    match_fecha = re.search(r'\b(\d{2}[/\-]\d{2}[/\-]\d{4}|\d{4}[/\-]\d{2}[/\-]\d{2})\b', texto)
    if match_fecha:
        datos["fecha"] = match_fecha.group(1)

    # 4. Extracción de montos decimales (busca números con dos decimales)
    # Filtra los montos encontrados en el texto
    montos_encontrados = re.findall(r'\b\d+[\.,]\d{2}\b', texto)
    if montos_encontrados:
        # Convertimos los valores a flotantes estándar reemplazando comas por puntos
        valores = sorted([float(v.replace(',', '.')) for v in montos_encontrados])
        
        # Asignación conservadora lógica para el prototipo:
        # El valor más alto suele ser el Total, y el menor suele ser el Neto o el Impuesto
        if len(valores) >= 2:
            datos["monto_total"] = valores[-1]
            datos["monto_neto"] = valores[-2] if len(valores) > 2 else valores[0]
            datos["impuesto"] = round(datos["monto_total"] - datos["monto_neto"], 2)
        else:
            datos["monto_total"] = valores[0]

    return datos

def validar_reglas_negocio(datos):
    """Valida los datos extraídos contra reglas de negocio simples."""
    errores = []
    
    if datos["fecha"] == "No detectada":
        errores.append("Falta definir la fecha de la factura.")
        
    if datos["numero_factura"] == "No detectado":
        errores.append("Falta definir el número o referencia de la factura.")
        
    # Validación matemática básica de consistencia
    if datos["monto_total"] > 0:
        calculo_total = round(datos["monto_neto"] + datos["impuesto"], 2)
        if abs(calculo_total - datos["monto_total"]) > 0.1:
            errores.append(
                f"Inconsistencia de montos: Neto ({datos['monto_neto']}) + Impuesto ({datos['impuesto']}) "
                f"no suma el Total ({datos['monto_total']})."
            )
            
    es_valido = len(errores) == 0
    return es_valido, errores

# --- Flujo Principal de Ejecución ---
if __name__ == "__main__":
    # Nombre de tu archivo local
    archivo_local = "factura.pdf"
    
    print(f"Buscando y procesando el archivo: {archivo_local}...")
    texto = extraer_texto_pdf(archivo_local)
    
    if texto:
        # OPCIONAL: Descomenta la línea de abajo si quieres ver todo el texto extraído del PDF
        # print("\n--- TEXTO EXTRAÍDO (DEBUG) ---\n", texto, "\n-----------------------------\n")
        
        # Procesar extracción
        datos = analizar_datos_factura(texto)
        
        # Validar resultados
        valido, errores = validar_reglas_negocio(datos)
        
        # Mostrar informe final
        print("\n================ RESULTADOS DEL PROTOTIPO ================")
        print(f"Proveedor:      {datos['proveedor']}")
        print(f"N° Factura:     {datos['numero_factura']}")
        print(f"Fecha:          {datos['fecha']}")
        print(f"Monto Neto:     ${datos['monto_neto']:.2f}")
        print(f"Impuesto:       ${datos['impuesto']:.2f}")
        print(f"Monto Total:    ${datos['monto_total']:.2f}")
        print("==========================================================")
        
        if valido:
            print("Resultado: [APROBADA] - Lista para procesar en Odoo.")
        else:
            print("Resultado: [RECHAZADA] - Se encontraron las siguientes observaciones:")
            for err in errores:
                print(f"  * {err}")