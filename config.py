import streamlit as st
import pandas as pd

# ----------------------------
# Configuración de la App
# ----------------------------
st.set_page_config(
    page_title="Bodega ALM - Inventario", 
    layout="wide",
    page_icon="📦",
    initial_sidebar_state="expanded"
)

# ----------------------------
# Inicialización de Session State
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "inventario" not in st.session_state:
    st.session_state.inventario = pd.DataFrame(
        columns=["ID", "Nombre", "Categoría", "Cantidad", "Precio", "Fecha_Agregado"]
    )

if "movimientos" not in st.session_state:
    st.session_state.movimientos = pd.DataFrame(
        columns=["ID_Movimiento", "Tipo", "Producto_ID", "Producto_Nombre", "Cantidad", "Fecha", "Usuario", "Observaciones"]
    )

# ----------------------------
# Usuarios autorizados
# ----------------------------
EMPLEADOS_AUTORIZADOS = {
    "admin": "123456",
    "carlos.rodriguez": "empleado123",
    "maria.gonzalez": "empleado456",
    "jose.martinez": "empleado789",
    "ana.lopez": "empleado321",
    "luis.torres": "empleado654"
}
