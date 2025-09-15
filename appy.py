import streamlit as st
import pandas as pd

# ----------------------------
# Configuración de la App
# ----------------------------
st.set_page_config(page_title="Bodega ALM - Inventario", layout="wide")

st.title("📦 Sistema de Gestión de Inventario - Bodega ALM")
st.markdown("Prototipo interactivo tipo **CRUD** desarrollado con Streamlit.")

# ----------------------------
# Datos iniciales (en memoria)
# ----------------------------
if "inventario" not in st.session_state:
    st.session_state.inventario = pd.DataFrame(columns=["ID", "Nombre", "Categoría", "Cantidad"])

inventario = st.session_state.inventario

# ----------------------------
# Funciones CRUD
# ----------------------------
def agregar_producto(id_, nombre, categoria, cantidad):
    nuevo = pd.DataFrame([[id_, nombre, categoria, cantidad]], 
                         columns=["ID", "Nombre", "Categoría", "Cantidad"])
    st.session_state.inventario = pd.concat([st.session_state.inventario, nuevo], ignore_index=True)

def eliminar_producto(id_):
    st.session_state.inventario = st.session_state.inventario[st.session_state.inventario["ID"] != id_]

def actualizar_producto(id_, nombre, categoria, cantidad):
    idx = st.session_state.inventario[st.session_state.inventario["ID"] == id_].index
    if not idx.empty:
        st.session_state.inventario.loc[idx[0], ["Nombre", "Categoría", "Cantidad"]] = [nombre, categoria, cantidad]

# ----------------------------
# Interfaz
# ----------------------------
menu = ["📋 Ver Inventario", "➕ Agregar Producto", "✏️ Actualizar Producto", "🗑️ Eliminar Producto"]
opcion = st.sidebar.radio("Menú", menu)

# Ver Inventario
if opcion == "📋 Ver Inventario":
    st.subheader("Inventario actual")
    st.dataframe(inventario, use_container_width=True)

# Agregar Producto
elif opcion == "➕ Agregar Producto":
    st.subheader("Agregar un nuevo producto")
    with st.form("form_agregar"):
        id_ = st.text_input("ID del producto")
        nombre = st.text_input("Nombre del producto")
        categoria = st.text_input("Categoría")
        cantidad = st.number_input("Cantidad", min_value=0, step=1)
        submit = st.form_submit_button("Agregar")

    if submit:
        if id_ and nombre:
            if id_ in inventario["ID"].values:
                st.warning("⚠️ Ya existe un producto con este ID.")
            else:
                agregar_producto(id_, nombre, categoria, cantidad)
                st.success(f"✅ Producto '{nombre}' agregado correctamente.")
        else:
            st.error("❌ Debes completar al menos ID y Nombre.")

# Actualizar Producto
elif opcion == "✏️ Actualizar Producto":
    st.subheader("Actualizar un producto")
    ids = inventario["ID"].tolist()
    if ids:
        id_sel = st.selectbox("Selecciona un producto por ID", ids)
        producto = inventario[inventario["ID"] == id_sel].iloc[0]

        with st.form("form_actualizar"):
            nombre = st.text_input("Nombre", producto["Nombre"])
            categoria = st.text_input("Categoría", producto["Categoría"])
            cantidad = st.number_input("Cantidad", min_value=0, value=int(producto["Cantidad"]), step=1)
            submit = st.form_submit_button("Actualizar")

        if submit:
            actualizar_producto(id_sel, nombre, categoria, cantidad)
            st.success("✅ Producto actualizado correctamente.")
    else:
        st.info("No hay productos en el inventario para actualizar.")

# Eliminar Producto
elif opcion == "🗑️ Eliminar Producto":
    st.subheader("Eliminar un producto")
    ids = inventario["ID"].tolist()
    if ids:
        id_sel = st.selectbox("Selecciona un producto por ID", ids)
        if st.button("Eliminar"):
            eliminar_producto(id_sel)
            st.success(f"✅ Producto con ID {id_sel} eliminado.")
    else:
        st.info("No hay productos en el inventario para eliminar.")
