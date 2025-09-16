import streamlit as st
import pandas as pd
from datetime import datetime

# Base de datos de usuarios
USUARIOS = {
    "admin": {"password": "admin123", "role": "Administrador", "name": "Administrador del Sistema"},
    "empleado1": {"password": "emp123", "role": "Empleado", "name": "Juan Pérez"},
    "empleado2": {"password": "emp456", "role": "Empleado", "name": "María García"},
    "supervisor": {"password": "sup123", "role": "Supervisor", "name": "Carlos López"}
}

# ----------------------------
# FUNCIONES DE AUTENTICACIÓN (agregar después de los imports)
# ----------------------------

def verificar_login(usuario, password):
    """Verifica las credenciales del usuario"""
    if usuario in USUARIOS:
        if USUARIOS[usuario]["password"] == password:
            return True, USUARIOS[usuario]["role"], USUARIOS[usuario]["name"]
    return False, None, None

def mostrar_login():
    """Muestra la página de login"""
    st.markdown("""
    <div class="main-header">
        <h1>🔐 Sistema de Autenticación</h1>
        <h3>Bodega A La Mano - Acceso Seguro</h3>
        <p>Ingrese sus credenciales para acceder al sistema</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 👤 Iniciar Sesión")
        
        with st.form("login_form"):
            usuario = st.text_input("👤 Usuario", placeholder="Ingrese su usuario")
            password = st.text_input("🔒 Contraseña", type="password", placeholder="Ingrese su contraseña")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                login_btn = st.form_submit_button("🚀 Iniciar Sesión", use_container_width=True)
            with col_btn2:
                demo_btn = st.form_submit_button("👁️ Ver Demo", use_container_width=True)
        
        if login_btn:
            if usuario and password:
                es_valido, rol, nombre = verificar_login(usuario, password)
                if es_valido:
                    st.session_state.logged_in = True
                    st.session_state.usuario = usuario
                    st.session_state.rol = rol
                    st.session_state.nombre = nombre
                    st.success(f"✅ ¡Bienvenido {nombre}!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Usuario o contraseña incorrectos")
            else:
                st.error("❌ Por favor complete todos los campos")
        
        if demo_btn:
            st.session_state.logged_in = True
            st.session_state.usuario = "demo"
            st.session_state.rol = "Demo"
            st.session_state.nombre = "Usuario Demo"
            st.success("✅ ¡Acceso demo activado!")
            st.rerun()
        
        # Información de usuarios de prueba
        st.markdown("---")
        st.markdown("### 💡 Usuarios de Prueba")
        st.info("""
        **Administrador:**
        - Usuario: `admin` | Contraseña: `admin123`
        
        **Empleados:**
        - Usuario: `empleado1` | Contraseña: `emp123`
        - Usuario: `empleado2` | Contraseña: `emp456`
        
        **Supervisor:**
        - Usuario: `supervisor` | Contraseña: `sup123`
        
        **O usa el botón "Ver Demo" para acceso rápido**
        """)

def cerrar_sesion():
    """Cierra la sesión del usuario"""
    st.session_state.logged_in = False
    if 'usuario' in st.session_state:
        del st.session_state.usuario
    if 'rol' in st.session_state:
        del st.session_state.rol
    if 'nombre' in st.session_state:
        del st.session_state.nombre
    st.rerun()



# ----------------------------
# Configuración de la App
# ----------------------------
st.set_page_config(
    page_title="Bodega ALM - Sistema de Inventario", 
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
        min-width: 150px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# VERIFICACIÓN DE AUTENTICACIÓN 
# ----------------------------

# Inicializar estado de login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Verificar si el usuario está logueado
if not st.session_state.logged_in:
    mostrar_login()
    st.stop()  # Detiene la ejecución del resto del código

# Header principal
usuario_actual = st.session_state.get('nombre', 'Usuario')
rol_actual = st.session_state.get('rol', 'Sin rol')

st.markdown(f"""
<div class="main-header">
    <h1>📦 Sistema de Gestión de Inventario</h1>
    <h3>Bodega A La Mano, siempre al alcance de tu mano.</h3>
    <p>Prototipo CRUD de gestión | Versión 2.0</p>
    <div style="margin-top: 1rem; padding: 0.5rem; background: rgba(255,255,255,0.2); border-radius: 5px;">
        <strong>👤 Usuario:</strong> {usuario_actual} | <strong>🎭 Rol:</strong> {rol_actual}
    </div>
</div>
""", unsafe_allow_html=True)


# ----------------------------
# Logo en el Sidebar (Panel de Control)
# ----------------------------
with st.sidebar:
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

    # Información del usuario
    st.markdown("## 👤 Usuario Activo")
    st.markdown(f"**Nombre:** {st.session_state.get('nombre', 'Usuario')}")
    st.markdown(f"**Rol:** {st.session_state.get('rol', 'Sin rol')}")
    st.markdown(f"**Usuario:** {st.session_state.get('usuario', 'N/A')}")
    
    # Botón de cerrar sesión
    if st.button("🚪 Cerrar Sesión", use_container_width=True, type="secondary"):
        cerrar_sesion()
    
    st.markdown("---")
    st.markdown("## 🛠️ Panel de Control")
    



# ----------------------------
# Datos iniciales (en memoria)
# ----------------------------
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

# ----------------------------
# Funciones CRUD
# ----------------------------
def Registrar_producto(id_, nombre, categoria, cantidad, precio):
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
# Sidebar con métricas
# ----------------------------
with st.sidebar:
    st.markdown("### 📊 Panel de Control")
    
    # Estadísticas
    total_productos, total_cantidad, valor_total, productos_bajo_stock = obtener_estadisticas()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📦 Productos", total_productos)
        st.metric("💰 Valor Total", f"S/{valor_total:,.2f}")
    
    with col2:
        st.metric("📈 Stock Total", total_cantidad)
        st.metric("⚠️ Bajo Stock", productos_bajo_stock, delta_color="inverse")
    
    st.markdown("---")
    
    # Menú de navegación
    st.markdown("### 🧭 Navegación")
    menu_options = {
        "📋 Dashboard": "dashboard",
        "🔎 Buscar Producto": "buscar",
        "➕ Registrar Producto": "Registrar",
        "✏️ Actualizar Producto": "actualizar", 
        "🗑️ Eliminar Producto": "eliminar",
        "📊 Reportes": "reportes"
    }
    
    opcion = st.radio("", list(menu_options.keys()), key="menu_radio")
    opcion_key = menu_options[opcion]

  # Menú de navegación con control de permisos
    st.markdown("### 🧭 Navegación")
    
    # Definir permisos por rol
    permisos = {
        "Administrador": ["dashboard", "buscar", "Registrar", "actualizar", "eliminar", "reportes"],
        "Supervisor": ["dashboard", "buscar", "Registrar", "actualizar", "reportes"],
        "Empleado": ["dashboard", "buscar", "Registrar"],
        "Demo": ["dashboard", "buscar", "reportes"]
    }
    
    rol_usuario = st.session_state.get('rol', 'Demo')
    permisos_usuario = permisos.get(rol_usuario, ["dashboard"])
    
    # Opciones de menú filtradas por permisos
    menu_options = {}
    if "dashboard" in permisos_usuario:
        menu_options["📋 Dashboard"] = "dashboard"
    if "buscar" in permisos_usuario:
        menu_options["🔎 Buscar Producto"] = "buscar"
    if "Registrar" in permisos_usuario:
        menu_options["➕ Registrar Producto"] = "Registrar"
    if "actualizar" in permisos_usuario:
        menu_options["✏️ Actualizar Producto"] = "actualizar"
    if "eliminar" in permisos_usuario:
        menu_options["🗑️ Eliminar Producto"] = "eliminar"
    if "reportes" in permisos_usuario:
        menu_options["📊 Reportes"] = "reportes"
    
    opcion = st.radio("", list(menu_options.keys()), key="menu_radio")
    opcion_key = menu_options[opcion]
    
    # Mostrar permisos del usuario
    st.markdown("---")
    st.markdown("### 🎭 Permisos del Rol")
    permisos_texto = {
        "dashboard": "📋 Ver Dashboard",
        "buscar": "🔎 Buscar Productos", 
        "Registrar": "➕ Registrar Productos",
        "actualizar": "✏️ Actualizar Productos",
        "eliminar": "🗑️ Eliminar Productos",
        "reportes": "📊 Ver Reportes"
    }
    
    for permiso in permisos_usuario:
        if permiso in permisos_texto:
            st.markdown(f"✅ {permisos_texto[permiso]}")
    
    # Mostrar permisos denegados
    todos_permisos = ["dashboard", "buscar", "Registrar", "actualizar", "eliminar", "reportes"]
    permisos_denegados = [p for p in todos_permisos if p not in permisos_usuario]
    
    if permisos_denegados:
        st.markdown("**Acceso Restringido:**")
        for permiso in permisos_denegados:
            if permiso in permisos_texto:
                st.markdown(f"❌ {permisos_texto[permiso]}")

# ----------------------------
# AGREGAR CONTROL DE PERMISOS EN LAS SECCIONES
# ----------------------------

# En cada sección (Registrar, actualizar, eliminar), agregar verificación de permisos.
# Por ejemplo, al inicio de la sección "Registrar Producto":

elif opcion_key == "Registrar":
    if "Registrar" not in permisos.get(st.session_state.get('rol', 'Demo'), []):
        st.error("❌ No tienes permisos para Registrar productos")
        st.info("💡 Contacta al administrador para obtener los permisos necesarios")
        st.stop()
    
    # El resto del código de Registrar se mantiene igual...

# Y similar para actualizar y eliminar:

elif opcion_key == "actualizar":
    if "actualizar" not in permisos.get(st.session_state.get('rol', 'Demo'), []):
        st.error("❌ No tienes permisos para actualizar productos")
        st.info("💡 Contacta al administrador para obtener los permisos necesarios")
        st.stop()
    
    # El resto del código de actualizar se mantiene igual...

elif opcion_key == "eliminar":
    if "eliminar" not in permisos.get(st.session_state.get('rol', 'Demo'), []):
        st.error("❌ No tienes permisos para eliminar productos")
        st.info("💡 Contacta al administrador para obtener los permisos necesarios")
        st.stop()

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
elif opcion_key == "Registrar":
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

# ----------------------------
# Footer
# ----------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>📦 <strong>Sistema de Inventario Bodega ALM</strong> | Desarrollado por el Grupo 5</p>
    <p><small>Versión 2.0 - Sin Dependencias Externas</small></p>
</div>
""", unsafe_allow_html=True)
