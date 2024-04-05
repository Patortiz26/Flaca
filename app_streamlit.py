import pandas as pd
import streamlit as st
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO

def df_to_pdf(df):
    # Crear un objeto BytesIO para el PDF
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=landscape(letter), rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    elements = []

    # Convertir DataFrame a una lista de listas para ReportLab
    data = [df.columns.tolist()] + df.values.tolist()
    table = Table(data, repeatRows=1)

    # Estilo de la tabla, incluyendo tamaño de fuente más pequeño
    table_style = TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
        ('BOX', (0,0), (-1,-1), 0.5, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('FONTSIZE', (0,0), (-1,-1), 8),  # Establecer el tamaño de la fuente aquí
    ])
    table.setStyle(table_style)

    elements.append(table)
    doc.build(elements)

    # Mover el puntero al inicio del BytesIO
    pdf_buffer.seek(0)
    return pdf_buffer

st.title('Programa Exclusivo Sandra Vargas')
st.write('Programa para el uso exclusivo de Sandra Vargas')
st.write('Desarrollado por Patricio Ortiz: ptricio.ortiz.v@ug.uchile.cl')

archivo_cargado = st.file_uploader("Sube un archivo Excel o CSV", type=['xlsx', 'csv'])
nombre_archivo_salida = st.text_input("Nombre del archivo de salida (sin extensión)", "datos_filtrados")

if archivo_cargado is not None:
    if archivo_cargado.name.endswith('.xlsx'):
        df = pd.read_excel(archivo_cargado)
    elif archivo_cargado.name.endswith('.csv'):
        df = pd.read_csv(archivo_cargado)
    
    columnas_a_mantener = ['Tipo Compra', 'RUT Proveedor', 'Razon Social', 'Folio', 'Fecha Docto', 'Monto Neto', 'Monto IVA Recuperable', 'Monto Total']
    
    if all(columna in df.columns for columna in columnas_a_mantener):
        df_filtrado = df[columnas_a_mantener]
        st.write(df_filtrado)
        
        # Crear un PDF a partir del DataFrame filtrado
        pdf_output = df_to_pdf(df_filtrado)
        
        st.download_button(label="Descargar PDF",
                           data=pdf_output,
                           file_name=f"{nombre_archivo_salida}.pdf",
                           mime="application/pdf")
    else:
        st.error("El archivo cargado no contiene todas las columnas requeridas.")
