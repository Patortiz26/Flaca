import streamlit as st
import pandas as pd
from io import BytesIO

# Función para convertir los datos a formato Excel
def a_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    df.to_excel(writer, index=False, sheet_name='Hoja1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

st.title('Selector de Columnas de Excel')

# Mensaje personalizado en la parte superior
st.header('Flaquita, te quiero mucho')

# Entrada para que el usuario especifique el nombre del archivo de salida
nombre_archivo_salida = st.text_input("Ingresa el nombre del archivo de salida sin la extensión", "ESCRIBE AQUI")

# Cargar archivo Excel
archivo_cargado = st.file_uploader("Elige un archivo", type=['xlsx'])
if archivo_cargado is not None:
    # Leer el archivo Excel
    df = pd.read_excel(archivo_cargado)
    
    # Columnas a mantener
    columnas_a_mantener = ['Tipo Compra', 'RUT Proveedor', 'Razon Social', 'Folio', 'Fecha Docto', 'Monto Neto', 'Monto IVA Recuperable', 'Monto Total']
    
    # Verificar si el archivo cargado contiene las columnas requeridas
    if all(columna in df.columns for columna in columnas_a_mantener):
        df_columnas_seleccionadas = df[columnas_a_mantener]
        
        st.write("Datos de las Columnas Seleccionadas:")
        st.dataframe(df_columnas_seleccionadas)
        
        # Enlace para descargar los datos filtrados
        df_xlsx = a_excel(df_columnas_seleccionadas)
        st.download_button(label='📥 Descargar Columnas Seleccionadas en Excel',
                           data=df_xlsx,
                           file_name=f'{nombre_archivo_salida}.xlsx')
    else:
        st.error("El archivo cargado no contiene las columnas requeridas.")
