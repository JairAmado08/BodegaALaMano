import streamlit as st
import pandas as pd
from datetime import datetime

# ----------------------------
# Pantalla de Login
# ----------------------------
if not st.session_state.logged_in:
    # Centrar el contenido de login
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="login-container">
            <h1>🏪 Bodega A La Mano</h1>
            <h3>Sistema de Inventario</h3>
            <p>Ingrese sus credenciales de empleado</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.markdown("### 🔐 Iniciar Sesión")
            
            username = st.text_input("👤 Usuario", placeholder="nombre.apellido")
            password = st.text_input("🔑 Contraseña", type="password", placeholder="Su contraseña")
            
            col_login1, col_login2 = st.columns(2)
            with col_login1:
                login_button = st.form_submit_button("🚀 Ingresar", use_container_width=True)
            
            if login_button:
                if username and password:
                    if login_user(username, password):
                        st.success("✅ ¡Bienvenido! Accediendo al sistema...")
                        st.rerun()
                    else:
                        st.error("❌ Usuario o contraseña incorrectos.")
                else:
                    st.warning("⚠️ Por favor, complete todos los campos.")
        
        # Información de usuarios de prueba
        with st.expander("👥 Usuarios de Prueba"):
            st.markdown("""
            **Empleados autorizados:**
            - `admin` / `123456`
            - `carlos.rodriguez` / `empleado123`
            - `maria.gonzalez` / `empleado456`
            - `jose.martinez` / `empleado789`
            - `ana.lopez` / `empleado321`
            - `luis.torres` / `empleado654`
            """)
    
    # Detener ejecución aquí si no está logueado
    st.stop()

# ----------------------------
# Sistema Principal (solo si está logueado)
# ----------------------------

# Header principal con bienvenida
display_name = get_display_name(st.session_state.username)
st.markdown(f"""
<div class="main-header">
    <h1>📦 Sistema de Gestión de Inventario</h1>
    <h3>Bodega A La Mano, siempre al alcance de tu mano.</h3>
    <p>¡Bienvenido/a, <strong>{display_name}</strong>! | Prototipo CRUD de gestión | Versión 2.5</p>
</div>
""", unsafe_allow_html=True)

# ----------------------------
# Datos iniciales (en memoria)
# ----------------------------

# Inicializar DataFrame de inventario
if "inventario" not in st.session_state:
    st.session_state.inventario = pd.DataFrame(columns=["ID", "Nombre", "Categoría", "Cantidad", "Precio", "Fecha_Agregado"])
    # Datos de ejemplo
    ejemplos = [
        ["P001", "Inca Kola 1.5L", "Bebidas", 15, 6.50, "2024-01-15"],
        ["P002", "Arroz Costeño 1kg", "Abarrotes secos", 25, 5.00, "2024-01-16"],
        ["P003", "Leche Gloria tarro", "Lácteos y derivados", 18, 4.80, "2024-01-17"],
        ["P004", "Pan francés (unidad)", "Panadería y repostería", 50, 0.40, "2024-01-18"],
        ["P005", "Atún Florida 170g", "Enlatados y conservas", 2, 6.00, "2024-01-19"]
    ]
    for ejemplo in ejemplos:
        nuevo = pd.DataFrame([ejemplo], columns=["ID", "Nombre", "Categoría", "Cantidad", "Precio", "Fecha_Agregado"])
        st.session_state.inventario = pd.concat([st.session_state.inventario, nuevo], ignore_index=True)

inventario = st.session_state.inventario

# Inicializar DataFrame de movimientos
if "movimientos" not in st.session_state:
    st.session_state.movimientos = pd.DataFrame(columns=["ID_Movimiento", "Tipo", "Producto_ID", "Producto_Nombre", "Cantidad", "Fecha", "Usuario", "Observaciones"])
    # Datos de ejemplo de movimientos
    movimientos_ejemplo = [
        ["M001", "Entrada", "P001", "Inca Kola 1.5L", 20, "2024-01-15", "admin", "Compra inicial"],
        ["M002", "Salida", "P001", "Inca Kola 1.5L", 5, "2024-01-16", "carlos.rodriguez", "Venta"],
        ["M003", "Entrada", "P002", "Arroz Costeño 1kg", 30, "2024-01-16", "maria.gonzalez", "Reposición"],
        ["M004", "Salida", "P002", "Arroz Costeño 1kg", 5, "2024-01-17", "jose.martinez", "Venta"],
        ["M005", "Ajuste", "P005", "Atún Florida 170g", -3, "2024-01-19", "admin", "Producto vencido"]
    ]
    for movimiento in movimientos_ejemplo:
        nuevo_mov = pd.DataFrame([movimiento], columns=["ID_Movimiento", "Tipo", "Producto_ID", "Producto_Nombre", "Cantidad", "Fecha", "Usuario", "Observaciones"])
        st.session_state.movimientos = pd.concat([st.session_state.movimientos, nuevo_mov], ignore_index=True)

movimientos = st.session_state.movimientos

# ----------------------------
# Sidebar (Panel de Control)
# ----------------------------
with st.sidebar:
    # Información del usuario logueado
    st.markdown(f"""
    <div class="user-info">
        <h4>👤 Usuario Activo</h4>
        <p><strong>{display_name}</strong></p>
        <p><small>Empleado de Bodega ALM</small></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Botón de cerrar sesión
    if st.button("🚪 Cerrar Sesión", use_container_width=True):
        logout_user()
    
    # Logo
    st.markdown(
        """
        <style>
        .sidebar-logo {
            display: flex;
            justify-content: center;
            width: 100%;
            margin-bottom: 1rem;
        }
        .sidebar-logo img {
            max-width: 150px;
            height: auto;
        }
        </style>
        <div class="sidebar-logo">
            <img src="https://raw.githubusercontent.com/JairAmado08/BodegaALaMano/main/images/ALMlogo.png">
        </div>
        """,
        unsafe_allow_html=True
    )

    # Encabezado principal
    st.markdown("## 🛠️ Panel de Control")

    # ----------------------------
    # Métricas
    # ----------------------------
    total_productos, total_cantidad, valor_total, productos_bajo_stock = obtener_estadisticas()

    st.markdown("### 📊 Estadísticas")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📦 Productos", total_productos)
        st.metric("💰 Valor Total", f"S/{valor_total:,.2f}")
    with col2:
        st.metric("📈 Stock Total", total_cantidad)
        st.metric("⚠️ Bajo Stock", productos_bajo_stock, delta_color="inverse")

    st.markdown("---")

    # ----------------------------
    # Navegación
    # ----------------------------
    st.markdown("### 🧭 Navegación")
    menu_options = {
        "📋 Dashboard de Inventario": "dashboard",
        "🔎 Buscar Producto": "buscar",
        "➕ Registrar Producto": "registrar",
        "✏️ Actualizar Producto": "actualizar", 
        "🗑️ Eliminar Producto": "eliminar",
        "📊 Reportes": "reportes",
        "📦 Dashboard de Movimientos": "movimientos_dashboard",
        "🔍 Buscar Movimiento": "buscar_movimiento",
        "➕ Registrar Movimiento": "registrar_movimiento",
        "✏️ Actualizar Movimiento": "actualizar_movimiento",
        "🗑️ Eliminar Movimiento": "eliminar_movimiento"
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

        # ----------------------------
        # Alertas de Stock Bajo
        # ----------------------------
        bajo_stock = inventario[inventario["Cantidad"] < 5]
        if not bajo_stock.empty:
            st.markdown("### 🔔 Alertas de Stock Bajo")
            for _, row in bajo_stock.iterrows():
                col1, col2, col3 = st.columns([2, 2, 1])   # 
                with col1:
                    st.markdown(
                        f"""
                        <div style="
                            background-color: #ff4d4d;
                            color: white;
                            padding: 10px;
                            border-radius: 8px;
                            margin-bottom: 8px;
                            font-weight: bold;">
                            🚨 <strong>{row['Nombre']}</strong> (ID: {row['ID']}) 
                    tiene solo <strong>{int(row['Cantidad'])}</strong> unidades en stock.
                </div>
                """,
                unsafe_allow_html=True
                    )
        else:
            st.markdown(
                '<div style="background-color: #4CAF50; color: white; padding: 10px; border-radius: 8px; font-weight: bold;">✅ No hay alertas de stock bajo.</div>',
                unsafe_allow_html=True
            )
        
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
            
            precio_total = cantidad * producto['Precio']
            
            st.markdown(f"""
            <div class="{card_class}">
                <div style="display: flex; justify-content: between; align-items: center;">
                    <div style="flex: 1;">
                        <h4>🏷️ {producto['Nombre']} (ID: {producto['ID']})</h4>
                        <p><strong>Categoría:</strong> {producto['Categoría']}</p>
                        <p><strong>Cantidad:</strong> {cantidad} unidades {stock_icon} <em>{stock_text}</em></p>
                        <p><strong>Precio unitario:</strong> S/{producto['Precio']:.2f}</p>
                        <p><strong>Valor total:</strong> S/{precio_total:.2f}</p>
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
                    format="S/%.2f"
                )
            }
        )
        
    else:
        st.info("📭 No hay productos en el inventario. ¡Comienza agregando algunos!")

# Registrar Producto
elif opcion_key == "registrar":
    st.markdown("## ➕ Registrar Nuevo Producto")
    
    with st.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.form("form_Registrar", clear_on_submit=True):
                st.markdown("### 📝 Información del Producto")
                
                col_form1, col_form2 = st.columns(2)
                with col_form1:
                    id_ = st.text_input("🆔 ID del producto", placeholder="Ej: P001")
                    nombre = st.text_input("🏷️ Nombre del producto", placeholder="Ej: Inca Kola 1.5L")
                    categoria = st.selectbox("📂 Categoría", 
                                           options=["Abarrotes secos", "Bebidas", "Lácteos y derivados", "Snacks y golosinas", "Panadería y repostería", "Cárnicos y embutidos", "Frutas y verduras",
                                            "Productos de limpieza e higiene personal", "Enlatados y conservas", "Aceites y salsas"],
                                           index=5)
                
                with col_form2:
                    cantidad = st.number_input("📦 Cantidad", min_value=0, step=1, value=1)
                    precio = st.number_input("💰 Precio unitario", min_value=0.0, step=0.01, format="%.2f")
                
                submit = st.form_submit_button("✅ Registrar Producto", use_container_width=True)
        
        with col2:
            st.markdown("### 💡 Consejos")
            st.info("""
            **Tips para Registrar productos:**
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
                Registrar_producto(id_, nombre, categoria, cantidad, precio)
                st.markdown('<div class="success-message">✅ Producto agregado correctamente.</div>', 
                          unsafe_allow_html=True)
                st.balloons()
        else:
            st.markdown('<div class="error-message">❌ Debes completar al menos ID y Nombre.</div>', 
                       unsafe_allow_html=True)

# Buscar Producto
elif opcion_key == "buscar":
    st.markdown("## 🔎 Buscar Producto en Inventario")
    
    busqueda = st.text_input("Ingrese nombre, ID o categoría del producto:")

    if busqueda:
        resultados = inventario[
            inventario["Nombre"].str.contains(busqueda, case=False, na=False) |
            inventario["ID"].astype(str).str.contains(busqueda, case=False, na=False) |
            inventario["Categoría"].str.contains(busqueda, case=False, na=False)
        ]
        
        if not resultados.empty:
            st.success(f"✅ Se encontraron {len(resultados)} productos que coinciden con '{busqueda}'.")
            
            st.dataframe(
                resultados,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Cantidad": st.column_config.NumberColumn("Cantidad", format="%d unidades"),
                    "Precio": st.column_config.NumberColumn("Precio", format="S/%.2f")
                }
            )
        else:
            st.error(f"⚠️ No se encontraron productos que coincidan con '{busqueda}'.")
    else:
        st.info("✍️ Escriba el nombre, ID o categoría para buscar un producto.")

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
                    
                    # Categorías unificadas con las de 'Registrar Producto'
                    categorias_lista = [
                        "Abarrotes secos", "Bebidas", "Lácteos y derivados", "Snacks y golosinas", 
                        "Panadería y repostería", "Cárnicos y embutidos", "Frutas y verduras",
                        "Productos de limpieza e higiene personal", "Enlatados y conservas", "Aceites y salsas"
                    ]
                    
                    # Determinar índice de la categoría actual si existe en la lista
                    if producto["Categoría"] in categorias_lista:
                        categoria_idx = categorias_lista.index(producto["Categoría"])
                    else:
                        categoria_idx = 0  # fallback por si la categoría no existe
                    
                    categoria = st.selectbox("📂 Categoría", options=categorias_lista, index=categoria_idx)
                
                with col_form2:
                    cantidad = st.number_input("📦 Cantidad", min_value=0, value=int(producto["Cantidad"]), step=1)
                    precio = st.number_input("💰 Precio", min_value=0.0, value=float(producto["Precio"]), step=0.01, format="%.2f")
                
                submit = st.form_submit_button("🔄 Actualizar Producto", use_container_width=True)

        
        with col2:
            st.markdown("### 📊 Información Actual")
            st.metric("📦 Cantidad Actual", int(producto["Cantidad"]))
            st.metric("💰 Precio Actual", f"S/{float(producto['Precio']):.2f}")
            st.metric("💎 Valor Total", f"S/{float(producto['Precio']) * int(producto['Cantidad']):.2f}")
        
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
                <p><strong>Precio:</strong> S/{float(producto['Precio']):.2f}</p>
                <p><strong>Valor Total:</strong> S/{float(producto['Precio']) * int(producto['Cantidad']):.2f}</p>
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
            total_productos = len(inventario)
            st.markdown(f"""
            <div class="stats-container">
                <h3>📦</h3>
                <h2>{total_productos}</h2>
                <p>Productos Únicos</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_unidades = int(inventario['Cantidad'].sum())
            st.markdown(f"""
            <div class="stats-container">
                <h3>📈</h3>
                <h2>{total_unidades}</h2>
                <p>Unidades Totales</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            valor_total = (inventario['Cantidad'] * inventario['Precio']).sum()
            st.markdown(f"""
            <div class="stats-container">
                <h3>💰</h3>
                <h2>S/{valor_total:,.0f}</h2>
                <p>Valor Inventario</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            total_categorias = inventario['Categoría'].nunique()
            st.markdown(f"""
            <div class="stats-container">
                <h3>🏷️</h3>
                <h2>{total_categorias}</h2>
                <p>Categorías</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Distribución por categorías
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
        inventario_valor["Cantidad"] = pd.to_numeric(inventario_valor["Cantidad"], errors="coerce")
        inventario_valor["Precio"] = pd.to_numeric(inventario_valor["Precio"], errors="coerce")
        inventario_valor["Valor_Total"] = inventario_valor["Cantidad"] * inventario_valor["Precio"]
        
        top_productos = inventario_valor.nlargest(5, "Valor_Total")
        
        st.dataframe(
            top_productos[['Nombre', 'Categoría', 'Cantidad', 'Precio', 'Valor_Total']],
            use_container_width=True,
            hide_index=True,
            column_config={
                "Precio": st.column_config.NumberColumn("Precio", format="S/%.2f"),
                "Valor_Total": st.column_config.NumberColumn("Valor Total", format="S/%.2f")
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
                    "Precio": st.column_config.NumberColumn("Precio", format="S/%.2f")
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
                "Precio": st.column_config.NumberColumn("Precio Promedio", format="S/%.2f"),
                "Valor_Categoria": st.column_config.NumberColumn("Valor Categoría", format="S/%.2f")
            }
        )
        
    else:
        st.info("📭 No hay datos suficientes para generar reportes.")

# Dashboard de Movimientos
elif opcion_key == "movimientos_dashboard":
    st.markdown("## 📦 Dashboard de Movimientos")
    
    # Estadísticas de movimientos
    total_movimientos, entradas, salidas, ajustes = obtener_estadisticas_movimientos()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 Total Movimientos", total_movimientos)
    with col2:
        st.metric("⬆️ Entradas", entradas)
    with col3:
        st.metric("⬇️ Salidas", salidas)
    with col4:
        st.metric("🔄 Ajustes/Devoluciones", ajustes)
    
    if not movimientos.empty:
        # Filtros
        col1, col2, col3 = st.columns(3)
        with col1:
            tipos = ['Todos'] + sorted(movimientos['Tipo'].unique().tolist())
            tipo_filtro = st.selectbox("🏷️ Filtrar por tipo:", tipos)
        
        with col2:
            productos_mov = ['Todos'] + sorted(movimientos['Producto_ID'].unique().tolist())
            producto_filtro = st.selectbox("📦 Filtrar por producto:", productos_mov)
        
        with col3:
            usuarios = ['Todos'] + sorted(movimientos['Usuario'].unique().tolist())
            usuario_filtro = st.selectbox("👤 Filtrar por usuario:", usuarios)
        
        # Aplicar filtros
        df_filtrado = movimientos.copy()
        if tipo_filtro != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['Tipo'] == tipo_filtro]
        if producto_filtro != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['Producto_ID'] == producto_filtro]
        if usuario_filtro != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['Usuario'] == usuario_filtro]
        
        # Mostrar movimientos
        st.markdown("### 📋 Historial de Movimientos")
        
        # Ordenar por fecha descendente
        df_filtrado = df_filtrado.sort_values('Fecha', ascending=False)
        
        for _, movimiento in df_filtrado.iterrows():
            # Determinar color según tipo de movimiento
            if movimiento['Tipo'] == 'Entrada':
                card_style = "border-left: 4px solid #28a745; background: #f8fff8;"
                icon = "⬆️"
            elif movimiento['Tipo'] == 'Salida':
                card_style = "border-left: 4px solid #dc3545; background: #fff5f5;"
                icon = "⬇️"
            elif movimiento['Tipo'] == 'Devolución':
                card_style = "border-left: 4px solid #17a2b8; background: #f0f8ff;"
                icon = "🔄"
            else:  # Ajuste
                card_style = "border-left: 4px solid #ffc107; background: #fffbf0;"
                icon = "⚖️"
            
            cantidad_text = f"+{movimiento['Cantidad']}" if movimiento['Cantidad'] > 0 else str(movimiento['Cantidad'])
            
            st.markdown(f"""
            <div class="product-card" style="{card_style}">
                <h4>{icon} {movimiento['Tipo']} - ID: {movimiento['ID_Movimiento']}</h4>
                <p><strong>Producto:</strong> {movimiento['Producto_Nombre']} ({movimiento['Producto_ID']})</p>
                <p><strong>Cantidad:</strong> {cantidad_text} unidades</p>
                <p><strong>Fecha:</strong> {movimiento['Fecha']}</p>
                <p><strong>Usuario:</strong> {movimiento['Usuario']}</p>
                <p><strong>Observaciones:</strong> {movimiento['Observaciones'] if movimiento['Observaciones'] else 'Sin observaciones'}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Vista detallada
        st.markdown("### 📋 Vista Detallada")
        st.dataframe(
            df_filtrado,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Cantidad": st.column_config.NumberColumn("Cantidad", format="%d"),
                "Fecha": st.column_config.DateColumn("Fecha")
            }
        )
    else:
        st.info("📭 No hay movimientos registrados.")

# Buscar Movimiento
elif opcion_key == "buscar_movimiento":
    st.markdown("## 🔍 Buscar Movimiento")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        busqueda = st.text_input("🔎 Ingrese ID de movimiento, tipo, producto o fecha:")
        
        if busqueda:
            resultados = movimientos[
                movimientos["ID_Movimiento"].str.contains(busqueda, case=False, na=False) |
                movimientos["Tipo"].str.contains(busqueda, case=False, na=False) |
                movimientos["Producto_ID"].str.contains(busqueda, case=False, na=False) |
                movimientos["Producto_Nombre"].str.contains(busqueda, case=False, na=False) |
                movimientos["Fecha"].str.contains(busqueda, case=False, na=False) |
                movimientos["Usuario"].str.contains(busqueda, case=False, na=False)
            ]
            
            if not resultados.empty:
                st.success(f"✅ Se encontraron {len(resultados)} movimientos que coinciden con '{busqueda}'.")
                
                st.dataframe(
                    resultados.sort_values('Fecha', ascending=False),
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Cantidad": st.column_config.NumberColumn("Cantidad", format="%d"),
                        "Fecha": st.column_config.DateColumn("Fecha")
                    }
                )
            else:
                st.error(f"⚠️ No se encontraron movimientos que coincidan con '{busqueda}'.")
        else:
            st.info("✍️ Escriba el ID, tipo, producto, fecha o usuario para buscar un movimiento de inventario.")
    
    with col2:
        st.markdown("### 💡 Tips de Búsqueda")
        st.info("""
        Puedes buscar por:
        - **ID:** M001, M002...
        - **Tipo:** Entrada, Salida, Ajuste, Devolución
        - **Producto:** P001, Inca Kola...
        - **Fecha:** 2024-01-15
        - **Usuario:** admin, carlos...
        """)
    
# Registrar Movimiento
elif opcion_key == "registrar_movimiento":
    st.markdown("## ➕ Registrar Nuevo Movimiento")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("form_registrar_movimiento", clear_on_submit=True):
            st.markdown("### 📝 Información del Movimiento")
            
            col_form1, col_form2 = st.columns(2)
            with col_form1:
                id_movimiento = st.text_input("🆔 ID del movimiento", placeholder="Ej: M001")
                tipo_movimiento = st.selectbox("🏷️ Tipo de movimiento", 
                                             options=["Entrada", "Salida", "Ajuste", "Devolución"])
                
                # Productos disponibles
                productos_disponibles = inventario["ID"].tolist() if not inventario.empty else []
                if productos_disponibles:
                    producto_seleccionado = st.selectbox("📦 Producto", productos_disponibles)
                else:
                    st.error("❌ No hay productos disponibles. Primero registra algunos productos.")
                    st.stop()
            
            with col_form2:
                if tipo_movimiento == "Ajuste":
                    cantidad = st.number_input("📊 Cantidad (+ para agregar, - para quitar)", 
                                             step=1, format="%d", help="Usa números negativos para ajustes de disminución")
                else:
                    cantidad = st.number_input("📊 Cantidad", min_value=1, step=1, value=1)
                
                observaciones = st.text_area("📝 Observaciones", placeholder="Comentarios adicionales...")
            
            submit = st.form_submit_button("✅ Registrar Movimiento", use_container_width=True)
    
    with col2:
        st.markdown("### 💡 Tipos de Movimiento")
        st.info("""
        **📥 Entrada:** Compras, recepciones
        
        **📤 Salida:** Ventas, entregas
        
        **⚖️ Ajuste:** Correcciones de inventario
        
        **🔄 Devolución:** Returns de clientes
        """)
        
        # Mostrar stock actual del producto seleccionado
        if 'producto_seleccionado' in locals():
            stock_actual = inventario[inventario["ID"] == producto_seleccionado]["Cantidad"].iloc[0]
            st.metric("📦 Stock Actual", int(stock_actual))
    
    if submit:
        if id_movimiento and productos_disponibles:
            if id_movimiento in movimientos["ID_Movimiento"].values:
                st.error("⚠️ Ya existe un movimiento con este ID.")
            else:
                registrar_movimiento(id_movimiento, tipo_movimiento, producto_seleccionado, cantidad, observaciones)
                st.success("✅ Movimiento registrado correctamente.")
                st.balloons()
        else:
            st.error("❌ Debes completar al menos ID y seleccionar un producto.")

# Actualizar Movimiento
elif opcion_key == "actualizar_movimiento":
    st.markdown("## ✏️ Actualizar Movimiento")
    
    ids_movimientos = movimientos["ID_Movimiento"].tolist()
    if ids_movimientos:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            id_mov_sel = st.selectbox("🔍 Selecciona un movimiento por ID", ids_movimientos)
            movimiento = movimientos[movimientos["ID_Movimiento"] == id_mov_sel].iloc[0]
            
            st.markdown(f"### 📋 Movimiento Actual: **{movimiento['ID_Movimiento']}**")
            
            with st.form("form_actualizar_movimiento"):
                st.markdown("#### 📝 Nuevos Datos")
                
                col_form1, col_form2 = st.columns(2)
                with col_form1:
                    tipo_movimiento = st.selectbox("🏷️ Tipo de movimiento", 
                                                 options=["Entrada", "Salida", "Ajuste", "Devolución"],
                                                 index=["Entrada", "Salida", "Ajuste", "Devolución"].index(movimiento["Tipo"]))
                    
                    productos_disponibles = inventario["ID"].tolist()
                    if movimiento["Producto_ID"] in productos_disponibles:
                        producto_idx = productos_disponibles.index(movimiento["Producto_ID"])
                    else:
                        producto_idx = 0
                    
                    producto_seleccionado = st.selectbox("📦 Producto", productos_disponibles, index=producto_idx)
                
                with col_form2:
                    cantidad = st.number_input("📊 Cantidad", value=int(movimiento["Cantidad"]), step=1)
                    fecha = st.date_input("📅 Fecha", value=pd.to_datetime(movimiento["Fecha"]).date())
                
                observaciones = st.text_area("📝 Observaciones", value=movimiento["Observaciones"])
                
                submit = st.form_submit_button("🔄 Actualizar Movimiento", use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Información Actual")
            st.info(f"""
            **Tipo:** {movimiento['Tipo']}
            
            **Producto:** {movimiento['Producto_Nombre']}
            
            **Cantidad:** {movimiento['Cantidad']}
            
            **Fecha:** {movimiento['Fecha']}
            
            **Usuario:** {movimiento['Usuario']}
            """)
        
        if submit:
            fecha_str = fecha.strftime("%Y-%m-%d")
            actualizar_movimiento(id_mov_sel, tipo_movimiento, producto_seleccionado, cantidad, fecha_str, observaciones)
            st.success("✅ Movimiento actualizado correctamente.")
            st.rerun()
    else:
        st.info("📭 No hay movimientos registrados para actualizar.")

# Eliminar Movimiento
elif opcion_key == "eliminar_movimiento":
    st.markdown("## 🗑️ Eliminar Movimiento")
    
    ids_movimientos = movimientos["ID_Movimiento"].tolist()
    if ids_movimientos:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            id_mov_sel = st.selectbox("🔍 Selecciona un movimiento por ID", ids_movimientos)
            movimiento = movimientos[movimientos["ID_Movimiento"] == id_mov_sel].iloc[0]
            
            st.markdown("### ⚠️ Movimiento a Eliminar")
            
            st.markdown(f"""
            <div class="product-card" style="border-left: 4px solid #dc3545; background: #fff5f5;">
                <h4>🏷️ {movimiento['ID_Movimiento']} - {movimiento['Tipo']}</h4>
                <p><strong>Producto:</strong> {movimiento['Producto_Nombre']} ({movimiento['Producto_ID']})</p>
                <p><strong>Cantidad:</strong> {movimiento['Cantidad']} unidades</p>
                <p><strong>Fecha:</strong> {movimiento['Fecha']}</p>
                <p><strong>Usuario:</strong> {movimiento['Usuario']}</p>
                <p><strong>Observaciones:</strong> {movimiento['Observaciones'] if movimiento['Observaciones'] else 'Sin observaciones'}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            confirmacion = st.checkbox(f"✅ Confirmo que deseo eliminar el movimiento **{movimiento['ID_Movimiento']}**")
            
            if confirmacion:
                if st.button("🗑️ ELIMINAR MOVIMIENTO", type="primary", use_container_width=True):
                    eliminar_movimiento(id_mov_sel)
                    st.success("✅ Movimiento eliminado correctamente.")
                    st.rerun()
        
        with col2:
            st.markdown("### ⚠️ Advertencia")
            st.warning("""
            **¡Atención!**
            
            Esta acción eliminará permanentemente el movimiento del historial.
            
            **El stock del producto NO se revertirá automáticamente.**
            
            Si necesitas revertir el stock, hazlo manualmente mediante un ajuste.
            """)
    else:
        st.info("📭 No hay movimientos registrados para eliminar.")

# ----------------------------
# Footer
# ----------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>📦 <strong>Sistema de Inventario Bodega ALM</strong> | Desarrollado por el Grupo 5</p>
    <p><small>Versión 2.5 - Sin Dependencias Externas</small></p>
</div>
""", unsafe_allow_html=True)

