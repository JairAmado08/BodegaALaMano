import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
    st.session_state.inventario = pd.DataFrame(columns=["ID", "Nombre", "Categoría", "Cantidad", "Precio"])

inventario = st.session_state.inventario

# ----------------------------
# Funciones CRUD
# ----------------------------
def agregar_producto(id_, nombre, categoria, cantidad, precio):
    nuevo = pd.DataFrame([[id_, nombre, categoria, cantidad, precio]],
                         columns=["ID", "Nombre", "Categoría", "Cantidad", "Precio"])
    st.session_state.inventario = pd.concat([st.session_state.inventario, nuevo], ignore_index=True)

def eliminar_producto(id_):
    st.session_state.inventario = st.session_state.inventario[st.session_state.inventario["ID"] != id_]

def actualizar_producto(id_, nombre, categoria, cantidad, precio):
    idx = st.session_state.inventario[st.session_state.inventario["ID"] == id_].index
    if not idx.empty:
        st.session_state.inventario.loc[idx[0], ["Nombre", "Categoría", "Cantidad", "Precio"]] = [nombre, categoria, cantidad, precio]

# ----------------------------
# Interfaz
# ----------------------------
menu = ["📋 Ver Inventario", "➕ Agregar Producto", "✏️ Actualizar Producto", "🗑️ Eliminar Producto", "📊 Reportes"]
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
        precio = st.number_input("Precio", min_value=0.0, step=0.1)
        submit = st.form_submit_button("Agregar")

    if submit:
        if id_ and nombre:
            if id_ in inventario["ID"].values:
                st.warning("⚠️ Ya existe un producto con este ID.")
            else:
                agregar_producto(id_, nombre, categoria, cantidad, precio)
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
            precio = st.number_input("Precio", min_value=0.0, value=float(producto["Precio"]), step=0.1)
            submit = st.form_submit_button("Actualizar")

        if submit:
            actualizar_producto(id_sel, nombre, categoria, cantidad, precio)
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

# Reportes
elif opcion == "📊 Reportes":
    st.subheader("Reportes de Inventario")

    if inventario.empty:
        st.info("⚠️ No hay datos en el inventario para generar reportes.")
    else:
        # Asegurar que las columnas numéricas sean realmente números
        inventario_valor = inventario.copy()
        inventario_valor["Cantidad"] = pd.to_numeric(inventario_valor["Cantidad"], errors="coerce").fillna(0)
        inventario_valor["Precio"] = pd.to_numeric(inventario_valor["Precio"], errors="coerce").fillna(0)

        # Calcular el valor total por producto
        inventario_valor["Valor_Total"] = inventario_valor["Cantidad"] * inventario_valor["Precio"]

        st.write("### 📌 Inventario con Valor Total")
        st.dataframe(inventario_valor, use_container_width=True)

        # Top 5 productos por valor
        st.write("### 🏆 Top 5 productos por valor en stock")
        top_productos = inventario_valor.nlargest(5, "Valor_Total")

        fig, ax = plt.subplots()
        ax.bar(top_productos["Nombre"], top_productos["Valor_Total"])
        ax.set_ylabel("Valor Total (S/.)")
        ax.set_xlabel("Producto")
        ax.set_title("Top 5 productos con mayor valor en stock")
        st.pyplot(fig)

        # Distribución por categoría
        st.write("### 📊 Distribución por Categoría")
        categoria_sum = inventario_valor.groupby("Categoría")["Cantidad"].sum()

        fig2, ax2 = plt.subplots()
        ax2.pie(categoria_sum, labels=categoria_sum.index, autopct="%1.1f%%", startangle=90)
        ax2.set_title("Distribución de productos por categoría")
        st.pyplot(fig2)
