from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generar_pdf_simulado(ruta_salida):
    try:
        # Configurar el lienzo de la página (tamaño carta)
        c = canvas.Canvas(ruta_salida, pagesize=letter)
        
        # Encabezado del Proveedor
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 730, "Reparaciones XL S.A.S.")
        c.setFont("Helvetica", 10)
        c.drawString(50, 715, "NIT: 900.123.456-1")
        c.drawString(50, 700, "Contacto: soporte@reparacionesxl.com")
        
        # Información de la factura
        c.setFont("Helvetica-Bold", 12)
        c.drawString(400, 730, "FACTURA DE VENTA")
        c.setFont("Helvetica", 10)
        c.drawString(400, 715, "Factura No: BILL-2025-004")
        c.drawString(400, 700, "Fecha: 15/02/2025")
        
        # Línea divisoria
        c.setLineWidth(1)
        c.line(50, 680, 550, 680)
        
        # Detalles del servicio
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, 650, "Descripción del Servicio")
        c.drawString(450, 650, "Valor")
        
        c.setFont("Helvetica", 10)
        c.drawString(50, 630, "Mantenimiento preventivo de infraestructura de servidores")
        c.drawString(450, 630, "1000.00")
        
        # Línea divisoria inferior
        c.line(50, 550, 550, 550)
        
        # Totales
        c.drawString(350, 530, "Monto Neto:")
        c.drawString(450, 530, "1000.00")
        
        c.drawString(350, 510, "Impuesto (IVA 19%):")
        c.drawString(450, 510, "190.00")
        
        c.setFont("Helvetica-Bold", 10)
        c.drawString(350, 490, "Monto Total:")
        c.drawString(450, 490, "1190.00")
        
        # Guardar archivo
        c.save()
        print(f"Archivo de prueba '{ruta_salida}' generado exitosamente.")
    except Exception as e:
        print(f"Error al generar el PDF de prueba: {e}")

if __name__ == "__main__":
    generar_pdf_simulado("factura.pdf")