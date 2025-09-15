import streamlit as st
import pandas as pd
from datetime import datetime

# ----------------------------
# Configuración de la App
# ----------------------------
st.set_page_config(
    page_title="Bodega ALM - Inventario", 
    layout="wide",
    page_icon="📦",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem; border-radius: 10px; margin-bottom: 2rem;
        color: white; text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);}
    .success-message { background-color: #d4edda; border: 1px solid #c3e6cb; color: #155724;
        padding: 0.75rem 1.25rem; margin-bottom: 1rem; border-radius: 0.25rem; border-left: 4px solid #28a745;}
    .warning-message { background-color: #fff3cd; border: 1px solid #ffeaa7; color: #856404;
        padding: 0.75rem 1.25rem; margin-bottom: 1rem; border-radius: 0.25rem; border-left: 4px solid #ffc107;}
    .error-message { background-color: #f8d7da; border: 1px solid #f5c6cb; color: #721c24;
        padding: 0.75rem 1.25rem; margin-bottom: 1rem; border-radius: 0.25rem; border-left: 4px solid #dc3545;}
    .product-card { background: white; padding: 1.5rem; border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin: 1rem 0; border: 1px solid #e9ecef;}
    .low-stock { border-left: 4px solid #dc3545 !important; background: #fff5f5 !important;}
    .medium-stock { border-left: 4px solid #ffc107 !important; background: #fffbf0 !important;}
    .good-stock { border-left: 4px solid #28a745 !important; background: #f8fff8 !important;}
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown("""
<div class="main-header">
    <h1>📦 Sistema de Gestión de Inventario</h1>
    <h3>Bodega ALM - Control Inteligente</h3>
    <p>Prototipo CRUD desarrollado con Streamlit | Versión 2.0</p>
</div>
""", unsafe_allow_html=True)

# ----------------------------
# Categorías de productos
# ----------------------------
CATEGORIAS = [
    "Abarrotes secos", "Bebidas", "Lácteos y derivados", "Snacks y golosinas",
    "Panadería y repostería", "Cárnicos y embutidos", "Frutas y verduras",
    "Productos de limpieza e higiene personal", "Enlatados y conservas", "Aceites y salsas"
]

# ----------------------------
# Datos iniciales
# ----------------------------
if "inventario" not in st.session_state:
    st.session_state.inventario = pd.DataFrame(columns=["ID", "Nombre", "Categoría", "Cantidad", "Precio", "Fecha_Agregado"])
    ejemplos = [
        ["P001", "Inca Kola 1.5L", "Bebidas", 15, 6.50, "2024-01-15"],
        ["P002", "Arroz Costeño 1kg", "Abarrotes secos", 25, 5.00, "2024-01-16"],
        ["P003", "Leche Gloria tarro", "Lácteos y derivados", 18, 4.80, "2024-01-17"],
        ["P004", "Pan francés (unidad)", "Panadería y repostería", 50, 0.40, "2024-01-18"],
        ["P005", "Atún Florida 170g", "Enlatados y conservas", 12, 6.00, "2024-01-19"]
    ]
    for ejemplo in ejemplos:
        nuevo = pd.DataFrame([ejemplo], columns=["ID", "Nombre", "Categoría", "Cantidad", "Precio", "Fecha_Agregado"])
        st.session_state.inventario = pd.concat([st.session_state.inventario, nuevo], ignore_index=True)

inventario = st.session_state.inventario

# ----------------------------
# Funciones CRUD
# ----------------------------
def agregar_producto(id_, nombre, categoria, cantidad, precio):
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    nuevo = pd.DataFrame([[id_, nombre, categoria, cantidad, precio, fecha_actual]], 
                         columns=["ID", "Nombre", "Categoría", "Cantidad", "Precio", "Fecha_Agregado"])
    st.session_state.inventario = pd.concat([st.session_state.inventario, nuevo], ignore_index=True)

def eliminar_producto(id_):
    st.session_state.inventario = st.session_state.inventario[st.session_state.inventario["ID"] != id_]

def actualizar_producto(id_, nombre, categoria, cantidad, precio):
    idx = st.session_state.inventario[st.session_state.inventario["ID"] == id_].index
    if not idx.empty:
        st.session_state.inventario.loc[idx[0], ["Nombre", "Categoría", "Cantidad", "Precio"]] = [nombre, categoria, cantidad, precio]

def obtener_estadisticas():
    if inventario.empty:
        return 0, 0, 0, 0
    total_productos = len(inventario)
    total_cantidad = inventario["Cantidad"].sum()
    valor_total = (inventario["Cantidad"] * inventario["Precio"]).sum()
    productos_bajo_stock = len(inventario[inventario["Cantidad"] < 5])
    return total_productos, total_cantidad, valor_total, productos_bajo_stock

# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:
    st.markdown("### 📊 Panel de Control")
    total_productos, total_cantidad, valor_total, productos_bajo_stock = obtener_estadisticas()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📦 Productos", total_productos)
        st.metric("💰 Valor Total", f"S/ {valor_total:,.2f}")
    with col2:
        st.metric("📈 Stock Total", total_cantidad)
        st.metric("⚠️ Bajo Stock", productos_bajo_stock, delta_color="inverse")
    st.markdown("---")
    st.markdown("### 🧭 Navegación")
    menu_options = {
        "📋 Dashboard": "dashboard",
        "➕ Agregar Producto": "agregar",
        "✏️ Actualizar Producto": "actualizar", 
        "🗑️ Eliminar Producto": "eliminar",
        "📊 Reportes": "reportes"
    }
    opcion = st.radio("", list(menu_options.keys()), key="menu_radio")
    opcion_key = menu_options[opcion]

# ----------------------------
# Dashboard
# ----------------------------
if opcion_key == "dashboard":
    st.subheader("📋 Inventario actual")
    st.dataframe(
        inventario,
        column_config={
            "Precio": st.column_config.NumberColumn("Precio", format="S/ %.2f"),
            "Cantidad": st.column_config.NumberColumn("Cantidad", format="%d"),
        },
        use_container_width=True
    )

# ----------------------------
# Agregar producto
# ----------------------------
elif opcion_key == "agregar":
    st.subheader("➕ Agregar Producto")
    with st.form("form_agregar"):
        id_ = st.text_input("ID del Producto")
        nombre = st.text_input("Nombre del Producto")
        categoria = st.selectbox("Categoría", CATEGORIAS)
        cantidad = st.number_input("Cantidad", min_value=0, value=0)
        precio = st.number_input("Precio (S/)", min_value=0.0, format="%.2f")
        submitted = st.form_submit_button("Agregar")
        if submitted:
            agregar_producto(id_, nombre, categoria, cantidad, precio)
            st.success(f"Producto **{nombre}** agregado con éxito ✅")

# ----------------------------
# Actualizar producto
# ----------------------------
elif opcion_key == "actualizar":
    st.subheader("✏️ Actualizar Producto")
    ids = inventario["ID"].tolist()
    if ids:
        id_sel = st.selectbox("Selecciona ID", ids)
        prod = inventario[inventario["ID"] == id_sel].iloc[0]
        with st.form("form_actualizar"):
            nombre = st.text_input("Nombre del Producto", prod["Nombre"])
            categoria = st.selectbox("Categoría", CATEGORIAS, index=CATEGORIAS.index(prod["Categoría"]))
            cantidad = st.number_input("Cantidad", min_value=0, value=int(prod["Cantidad"]))
            precio = st.number_input("Precio (S/)", min_value=0.0, format="%.2f", value=float(prod["Precio"]))
            submitted = st.form_submit_button("Actualizar")
            if submitted:
                actualizar_producto(id_sel, nombre, categoria, cantidad, precio)
                st.success(f"Producto **{nombre}** actualizado con éxito ✅")
    else:
        st.warning("No hay productos para actualizar.")

# ----------------------------
# Eliminar producto
# ----------------------------
elif opcion_key == "eliminar":
    st.subheader("🗑️ Eliminar Producto")
    ids = inventario["ID"].tolist()
    if ids:
        id_sel = st.selectbox("Selecciona ID", ids)
        if st.button("Eliminar"):
            eliminar_producto(id_sel)
            st.success(f"Producto con ID **{id_sel}** eliminado ✅")
    else:
        st.warning("No hay productos para eliminar.")

# ----------------------------
# Reportes
# ----------------------------
elif opcion_key == "reportes":
    st.subheader("📊 Reportes")
    if not inventario.empty:
        inventario["Valor_Total"] = inventario["Cantidad"] * inventario["Precio"]

        st.write("### 🔝 Top 5 productos por valor")
        top_productos = inventario.nlargest(5, "Valor_Total")
        st.dataframe(top_productos, use_container_width=True)

        st.write("### 📦 Stock por categoría")
        stock_categoria = inventario.groupby("Categoría")["Cantidad"].sum().reset_index()
        st.bar_chart(stock_categoria.set_index("Categoría"))
    else:
        st.info("No hay datos en el inventario para mostrar reportes.")


# ----------------------------
# Footer
# ----------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>📦 <strong>Sistema de Inventario Bodega ALM</strong> | Desarrollado con ❤️ usando Streamlit</p>
    <p><small>Versión 2.0 - Sin Dependencias Externas</small></p>
</div>
""", unsafe_allow_html=True)
