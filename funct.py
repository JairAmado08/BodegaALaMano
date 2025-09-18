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

