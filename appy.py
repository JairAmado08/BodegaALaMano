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

# CSS personalizado para mejorar el diseño
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    
    .success-message {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 0.75rem 1.25rem;
        margin-bottom: 1rem;
        border-radius: 0.25rem;
        border-left: 4px solid #28a745;
    }
    
    .warning-message {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 0.75rem 1.25rem;
        margin-bottom: 1rem;
        border-radius: 0.25rem;
        border-left: 4px solid #ffc107;
    }
    
    .error-message {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 0.75rem 1.25rem;
        margin-bottom: 1rem;
        border-radius: 0.25rem;
        border-left: 4px solid #dc3545;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    .product-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border: 1px solid #e9ecef;
    }
    
    .low-stock {
        border-left: 4px solid #dc3545 !important;
        background: #fff5f5 !important;
    }
    
    .medium-stock {
        border-left: 4px solid #ffc107 !important;
        background: #fffbf0 !important;
    }
    
    .good-stock {
        border-left: 4px solid #28a745 !important;
        background: #f8fff8 !important;
    }
    
    .stats-container {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .category-bar {
        background: #e9ecef;
        border-radius: 10px;
        margin: 0.5rem 0;
        overflow: hidden;
    }
    
    .category-fill {
        height: 30px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        padding: 0 10px;
        color: white;
        font-weight: bold;
    }
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
# Datos iniciales (en memoria)
# ----------------------------
if "inventario" not in st.session_state:
    st.session_state.inventario = pd.DataFrame(columns=["ID", "Nombre", "Categoría", "Cantidad", "Precio", "Fecha_Agregado"])
    # Datos de ejemplo
    ejemplos = [
        ["P001", "Laptop Dell", "Electrónicos", 15, 899.99, "2024-01-15"],
        ["P002", "Mesa de Oficina", "Muebles", 8, 299.99, "2024-01-16"],
        ["P003", "Café Premium", "Alimentos", 25, 12.99, "2024-01-17"],
        ["P004", "Impresora HP", "Electrónicos", 3, 199.99, "2024-01-18"],
        ["P005", "Silla Ergonómica", "Muebles", 12, 159.99, "2024-01-19"]
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
    valor_total = (inventario["Cantidad"] * inventario["Precio"]).sum() if "Precio" in inventario.columns else 0
    productos_bajo_stock = len(inventario[inventario["Cantidad"] < 5])
    
    return total_productos, total_cantidad, valor_total, productos_bajo_stock

# ----------------------------
# Sidebar con métricas
# ----------------------------
with st.sidebar:
    st.markdown("### 📊 Panel de Control")
    
    # Estadísticas
    total_productos, total_cantidad, valor_total, productos_bajo_stock = obtener_estadisticas()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📦 Productos", total_productos)
        st.metric("💰 Valor Total", f"${valor_total:,.2f}")
    
    with col2:
        st.metric("📈 Stock Total", total_cantidad)
        st.metric("⚠️ Bajo Stock", productos_bajo_stock, delta_color="inverse")
    
    st.markdown("---")
    
    # Menú de navegación
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
# Contenido principal
# ----------------------------

# Dashboard / Ver Inventario
if opcion_key == "dashboard":
    st.markdown("## 📋 Dashboard de Inventario")
    
    if not inventario.empty:
        # Filtros
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            categorias = ['Todas'] + sorted(inventario['Categoría'].unique().tolist())
            categoria_filtro = st.selectbox("🏷️ Filtrar por categoría:", categorias)
        
        with col2:
            stock_filtro = st.selectbox("📊 Filtrar por stock:", 
                                      ['Todos', 'Stock bajo (<5)', 'Stock medio (5-15)', 'Stock alto (>15)'])
        
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔄 Actualizar", use_container_width=True):
                st.rerun()
        
        # Aplicar filtros
        df_filtrado = inventario.copy()
        if categoria_filtro != 'Todas':
            df_filtrado = df_filtrado[df_filtrado['Categoría'] == categoria_filtro]
        
        if stock_filtro == 'Stock bajo (<5)':
            df_filtrado = df_filtrado[df_filtrado['Cantidad'] < 5]
        elif stock_filtro == 'Stock medio (5-15)':
            df_filtrado = df_filtrado[(df_filtrado['Cantidad'] >= 5) & (df_filtrado['Cantidad'] <= 15)]
        elif stock_filtro == 'Stock alto (>15)':
            df_filtrado = df_filtrado[df_filtrado['Cantidad'] > 15]
        
        # Mostrar productos como cards
        st.markdown("### 🏪 Productos en Inventario")
        
        for idx, producto in df_filtrado.iterrows():
            # Determinar el estado del stock
            cantidad = producto['Cantidad']
            if cantidad < 5:
                card_class = "product-card low-stock"
                stock_icon = "🔴"
                stock_text = "Stock Bajo"
            elif cantidad <= 15:
                card_class = "product-card medium-stock" 
                stock_icon = "🟡"
                stock_text = "Stock Medio"
            else:
                card_class = "product-card good-stock"
                stock_icon = "🟢"
                stock_text = "Stock Bueno"
            
            precio_total = cantidad * producto['Precio'] if 'Precio' in producto else 0
            
            st.markdown(f"""
            <div class="{card_class}">
                <div style="display: flex; justify-content: between; align-items: center;">
                    <div style="flex: 1;">
                        <h4>🏷️ {producto['Nombre']} (ID: {producto['ID']})</h4>
                        <p><strong>Categoría:</strong> {producto['Categoría']}</p>
                        <p><strong>Cantidad:</strong> {cantidad} unidades {stock_icon} <em>{stock_text}</em></p>
                        <p><strong>Precio unitario:</strong> ${producto['Precio']:.2f}</p>
                        <p><strong>Valor total:</strong> ${precio_total:.2f}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Tabla detallada
        st.markdown("### 📋 Vista Detallada")
        st.dataframe(
            df_filtrado,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Cantidad": st.column_config.NumberColumn(
                    "Cantidad",
                    help="Cantidad en stock",
                    format="%d unidades"
                ),
                "Precio": st.column_config.NumberColumn(
                    "Precio",
                    help="Precio por unidad",
                    format="$%.2f"
                )
            }
        )
        
    else:
        st.info("📭 No hay productos en el inventario. ¡Comienza agregando algunos!")

# Agregar Producto
elif opcion_key == "agregar":
    st.markdown("## ➕ Agregar Nuevo Producto")
    
    with st.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.form("form_agregar", clear_on_submit=True):
                st.markdown("### 📝 Información del Producto")
                
                col_form1, col_form2 = st.columns(2)
                with col_form1:
                    id_ = st.text_input("🆔 ID del producto", placeholder="Ej: P001")
                    nombre = st.text_input("🏷️ Nombre del producto", placeholder="Ej: Laptop Dell")
                    categoria = st.selectbox("📂 Categoría", 
                                           options=["Electrónicos", "Muebles", "Alimentos", "Ropa", "Herramientas", "Otros"],
                                           index=5)
                
                with col_form2:
                    cantidad = st.number_input("📦 Cantidad", min_value=0, step=1, value=1)
                    precio = st.number_input("💰 Precio unitario", min_value=0.0, step=0.01, format="%.2f")
                
                submit = st.form_submit_button("✅ Agregar Producto", use_container_width=True)
        
        with col2:
            st.markdown("### 💡 Consejos")
            st.info("""
            **Tips para agregar productos:**
            - Usa IDs únicos y descriptivos
            - Categoriza correctamente para mejor organización
            - Revisa el stock mínimo recomendado
            - Verifica el precio antes de guardar
            """)
    
    if submit:
        if id_ and nombre:
            if id_ in inventario["ID"].values:
                st.markdown('<div class="warning-message">⚠️ Ya existe un producto con este ID.</div>', 
                          unsafe_allow_html=True)
            else:
                agregar_producto(id_, nombre, categoria, cantidad, precio)
                st.markdown('<div class="success-message">✅ Producto agregado correctamente.</div>', 
                          unsafe_allow_html=True)
                st.balloons()
        else:
            st.markdown('<div class="error-message">❌ Debes completar al menos ID y Nombre.</div>', 
                       unsafe_allow_html=True)

# Actualizar Producto
elif opcion_key == "actualizar":
    st.markdown("## ✏️ Actualizar Producto")
    
    ids = inventario["ID"].tolist()
    if ids:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            id_sel = st.selectbox("🔍 Selecciona un producto por ID", ids)
            producto = inventario[inventario["ID"] == id_sel].iloc[0]
            
            # Mostrar información actual
            st.markdown(f"### 📋 Producto Actual: **{producto['Nombre']}**")
            
            with st.form("form_actualizar"):
                st.markdown("#### 📝 Nuevos Datos")
                
                col_form1, col_form2 = st.columns(2)
                with col_form1:
                    nombre = st.text_input("🏷️ Nombre", value=producto["Nombre"])
                    categoria = st.selectbox("📂 Categoría", 
                                           options=["Electrónicos", "Muebles", "Alimentos", "Ropa", "Herramientas", "Otros"],
                                           index=["Electrónicos", "Muebles", "Alimentos", "Ropa", "Herramientas", "Otros"].index(producto["Categoría"]) if producto["Categoría"] in ["Electrónicos", "Muebles", "Alimentos", "Ropa", "Herramientas", "Otros"] else 5)
                
                with col_form2:
                    cantidad = st.number_input("📦 Cantidad", min_value=0, value=int(producto["Cantidad"]), step=1)
                    precio = st.number_input("💰 Precio", min_value=0.0, value=float(producto["Precio"]) if "Precio" in producto else 0.0, step=0.01, format="%.2f")
                
                submit = st.form_submit_button("🔄 Actualizar Producto", use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Información Actual")
            st.metric("📦 Cantidad Actual", int(producto["Cantidad"]))
            if "Precio" in producto:
                st.metric("💰 Precio Actual", f"${float(producto['Precio']):.2f}")
                st.metric("💎 Valor Total", f"${float(producto['Precio']) * int(producto['Cantidad']):.2f}")
        
        if submit:
            actualizar_producto(id_sel, nombre, categoria, cantidad, precio)
            st.markdown('<div class="success-message">✅ Producto actualizado correctamente.</div>', 
                       unsafe_allow_html=True)
            st.rerun()
    else:
        st.info("📭 No hay productos en el inventario para actualizar.")

# Eliminar Producto
elif opcion_key == "eliminar":
    st.markdown("## 🗑️ Eliminar Producto")
    
    ids = inventario["ID"].tolist()
    if ids:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            id_sel = st.selectbox("🔍 Selecciona un producto por ID", ids)
            producto = inventario[inventario["ID"] == id_sel].iloc[0]
            
            # Mostrar información del producto a eliminar
            st.markdown(f"### ⚠️ Producto a Eliminar")
            
            st.markdown(f"""
            <div class="product-card" style="border-left: 4px solid #dc3545; background: #fff5f5;">
                <h4>🏷️ {producto['Nombre']} (ID: {producto['ID']})</h4>
                <p><strong>Categoría:</strong> {producto['Categoría']}</p>
                <p><strong>Cantidad:</strong> {int(producto['Cantidad'])} unidades</p>
                <p><strong>Precio:</strong> ${float(producto['Precio']):.2f}</p>
                <p><strong>Valor Total:</strong> ${float(producto['Precio']) * int(producto['Cantidad']):.2f}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Confirmación con checkbox
            confirmacion = st.checkbox(f"✅ Confirmo que deseo eliminar el producto **{producto['Nombre']}**")
            
            if confirmacion:
                if st.button("🗑️ ELIMINAR PRODUCTO", type="primary", use_container_width=True):
                    eliminar_producto(id_sel)
                    st.markdown('<div class="success-message">✅ Producto eliminado correctamente.</div>', 
                               unsafe_allow_html=True)
                    st.rerun()
        
        with col2:
            st.markdown("### ⚠️ Advertencia")
            st.warning("""
            **¡Atención!**
            
            Esta acción eliminará permanentemente el producto del inventario.
            
            **No se puede deshacer.**
            
            Asegúrate de que realmente quieres eliminar este producto.
            """)
            
    else:
        st.info("📭 No hay productos en el inventario para eliminar.")

# Reportes
elif opcion_key == "reportes":
    st.markdown("## 📊 Reportes y Análisis")
    
    if not inventario.empty:
        # Resumen general
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="stats-container">
                <h3>📦</h3>
                <h2>{}</h2>
                <p>Productos Únicos</p>
            </div>
            """.format(len(inventario)), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="stats-container">
                <h3>📈</h3>
                <h2>{}</h2>
                <p>Unidades Totales</p>
            </div>
            """.format(int(inventario['Cantidad'].sum())), unsafe_allow_html=True)
        
        with col3:
            valor_total = (inventario['Cantidad'] * inventario['Precio']).sum()
            st.markdown("""
            <div class="stats-container">
                <h3>💰</h3>
                <h2>${:,.0f}</h2>
                <p>Valor Inventario</p>
            </div>
            """.format(valor_total), unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="stats-container">
                <h3>🏷️</h3>
                <h2>{}</h2>
                <p>Categorías</p>
            </div>
            """.format(inventario['Categoría'].nunique()), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Distribución por categorías (gráfico simple)
        st.markdown("### 📊 Distribución por Categorías")
        categoria_counts = inventario['Categoría'].value_counts()
        max_count = categoria_counts.max()
        
        for categoria, count in categoria_counts.items():
            porcentaje = (count / len(inventario)) * 100
            width_percent = (count / max_count) * 100
            
            st.markdown(f"""
            <div class="category-bar">
                <div class="category-fill" style="width: {width_percent}%;">
                    {categoria}: {count} productos ({porcentaje:.1f}%)
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Top productos por valor
        st.markdown("### 💎 Top Productos por Valor")
        inventario_valor = inventario.copy()
        inventario_valor['Valor_Total'] = inventario_valor['Cantidad'] * inventario_valor['Precio']
        top_productos = inventario_valor.nlargest(5, 'Valor_Total')
        
        st.dataframe(
            top_productos[['Nombre', 'Categoría', 'Cantidad', 'Precio', 'Valor_Total']],
            use_container_width=True,
            hide_index=True,
            column_config={
                "Precio": st.column_config.NumberColumn("Precio", format="$%.2f"),
                "Valor_Total": st.column_config.NumberColumn("Valor Total", format="$%.2f")
            }
        )
        
        # Productos con stock bajo
        st.markdown("### ⚠️ Productos con Stock Bajo")
        productos_bajo_stock = inventario[inventario['Cantidad'] < 5]
        
        if not productos_bajo_stock.empty:
            st.dataframe(
                productos_bajo_stock,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Cantidad": st.column_config.NumberColumn(
                        "Cantidad",
                        help="⚠️ Stock bajo - requiere reabastecimiento",
                        format="%d unidades"
                    ),
                    "Precio": st.column_config.NumberColumn("Precio", format="$%.2f")
                }
            )
        else:
            st.success("🎉 ¡Todos los productos tienen stock adecuado!")
        
        # Análisis por categoría
        st.markdown("### 📈 Análisis por Categoría")
        analisis_categoria = inventario.groupby('Categoría').agg({
            'Cantidad': 'sum',
            'Precio': 'mean'
        }).round(2)
        analisis_categoria['Valor_Categoria'] = inventario.groupby('Categoría').apply(
            lambda x: (x['Cantidad'] * x['Precio']).sum()
        ).round(2)
        
        st.dataframe(
            analisis_categoria,
            use_container_width=True,
            column_config={
                "Cantidad": st.column_config.NumberColumn("Total Unidades", format="%d"),
                "Precio": st.column_config.NumberColumn("Precio Promedio", format="$%.2f"),
                "Valor_Categoria": st.column_config.NumberColumn("Valor Categoría", format="$%.2f")
            }
        )
        
    else:
        st.info("📭 No hay datos suficientes para generar reportes.")

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
</div>
""", unsafe_allow_html=True)
