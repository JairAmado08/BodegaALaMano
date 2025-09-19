
# ----------------------------
# Funciones Login
# ----------------------------

def login_user(username, password):
    """Función para autenticar usuario"""
    if username in EMPLEADOS_AUTORIZADOS and EMPLEADOS_AUTORIZADOS[username] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        return True
    return False

def logout_user():
    """Función para cerrar sesión"""
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

def get_display_name(username):
    """Convertir username en nombre para mostrar"""
    name_map = {
        "admin": "Administrador",
        "carlos.rodriguez": "Carlos Rodríguez",
        "maria.gonzalez": "María González", 
        "jose.martinez": "José Martínez",
        "ana.lopez": "Ana López",
        "luis.torres": "Luis Torres"
    }
    return name_map.get(username, username.replace(".", " ").title())
# ----------------------------
# Funciones CRUD para Inventario
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
# Funciones CRUD para Movimientos
# ----------------------------

def registrar_movimiento(id_mov, tipo, producto_id, cantidad, observaciones=""):
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    
    # Obtener nombre del producto
    producto_info = inventario[inventario["ID"] == producto_id]
    if not producto_info.empty:
        producto_nombre = producto_info.iloc[0]["Nombre"]
    else:
        producto_nombre = "Producto no encontrado"
    
    nuevo_movimiento = pd.DataFrame([[id_mov, tipo, producto_id, producto_nombre, cantidad, fecha_actual, st.session_state.username, observaciones]], 
                                   columns=["ID_Movimiento", "Tipo", "Producto_ID", "Producto_Nombre", "Cantidad", "Fecha", "Usuario", "Observaciones"])
    st.session_state.movimientos = pd.concat([st.session_state.movimientos, nuevo_movimiento], ignore_index=True)
    
    # Actualizar inventario según el tipo de movimiento
    if tipo in ["Entrada", "Devolución"]:
        actualizar_stock_producto(producto_id, cantidad)
    elif tipo in ["Salida", "Ajuste"] and cantidad < 0:
        actualizar_stock_producto(producto_id, cantidad)
    elif tipo == "Salida":
        actualizar_stock_producto(producto_id, -cantidad)

def actualizar_stock_producto(producto_id, cantidad_cambio):
    """Actualiza el stock del producto según el movimiento"""
    idx = inventario[inventario["ID"] == producto_id].index
    if not idx.empty:
        nueva_cantidad = max(0, inventario.loc[idx[0], "Cantidad"] + cantidad_cambio)
        st.session_state.inventario.loc[idx[0], "Cantidad"] = nueva_cantidad

def eliminar_movimiento(id_movimiento):
    """Elimina un movimiento (sin revertir cambios de stock)"""
    st.session_state.movimientos = st.session_state.movimientos[st.session_state.movimientos["ID_Movimiento"] != id_movimiento]

def actualizar_movimiento(id_mov, tipo, producto_id, cantidad, fecha, observaciones):
    """Actualiza los datos de un movimiento"""
    idx = st.session_state.movimientos[st.session_state.movimientos["ID_Movimiento"] == id_mov].index
    if not idx.empty:
        # Obtener nombre del producto
        producto_info = inventario[inventario["ID"] == producto_id]
        producto_nombre = producto_info.iloc[0]["Nombre"] if not producto_info.empty else "Producto no encontrado"
        
        st.session_state.movimientos.loc[idx[0], ["Tipo", "Producto_ID", "Producto_Nombre", "Cantidad", "Fecha", "Observaciones"]] = [tipo, producto_id, producto_nombre, cantidad, fecha, observaciones]

def obtener_estadisticas_movimientos():
    """Obtiene estadísticas de movimientos"""
    if movimientos.empty:
        return 0, 0, 0, 0
    
    total_movimientos = len(movimientos)
    entradas = len(movimientos[movimientos["Tipo"] == "Entrada"])
    salidas = len(movimientos[movimientos["Tipo"] == "Salida"])
    ajustes = len(movimientos[movimientos["Tipo"].isin(["Ajuste", "Devolución"])])
    
    return total_movimientos, entradas, salidas, ajustes
