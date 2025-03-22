import streamlit as st
from db_utils import get_tables

st.title("Inspector de Esquema de Base de Datos")

if st.button("Cargar tablas"):
    try:
        tables = get_tables()
        st.success(f"Se encontraron {len(tables)} tablas.")
        st.write(tables)
    except Exception as e:
        st.error(f"Error al conectar: {e}")
