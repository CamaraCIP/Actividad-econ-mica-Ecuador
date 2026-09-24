import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Actividad económica del Ecuador",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Actividad económica del Ecuador")
st.caption("Dashboard interactivo - Cámara de Industrias y Producción")

archivo = "data/base_dashboard_actividad_economica_ecuador.xlsx"

# Cargar hojas del archivo
pib = pd.read_excel(archivo, sheet_name="01_PIB_trimestral")
contribucion = pd.read_excel(archivo, sheet_name="02_Contribucion_PIB")
componentes = pd.read_excel(archivo, sheet_name="03_Componentes_PIB")
industrias = pd.read_excel(archivo, sheet_name="04_Industrias")
proyecciones = pd.read_excel(archivo, sheet_name="05_Proyecciones")

st.success("La base de datos se cargó correctamente.")

st.subheader("Prueba de lectura de la base")

opcion = st.selectbox(
    "Selecciona una base:",
    [
        "PIB trimestral",
        "Contribución al PIB",
        "Componentes del PIB",
        "Industrias",
        "Proyecciones"
    ]
)

if opcion == "PIB trimestral":
    st.dataframe(pib, use_container_width=True)

elif opcion == "Contribución al PIB":
    st.dataframe(contribucion, use_container_width=True)

elif opcion == "Componentes del PIB":
    st.dataframe(componentes, use_container_width=True)

elif opcion == "Industrias":
    st.dataframe(industrias, use_container_width=True)

elif opcion == "Proyecciones":
    st.dataframe(proyecciones, use_container_width=True)
