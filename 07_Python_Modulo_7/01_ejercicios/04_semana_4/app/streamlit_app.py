import streamlit as st
import requests

API_BASE_URL = "http://localhost:8000/api/v1"

st.set_page_config(page_title="Gestión de Cuentas", page_icon="🔐")
st.title("Sistema de Gestión de Cuentas")

menu = ["Registro", "Login"]
choice = st.sidebar.selectbox("Menú", menu)

# Inicializar variables de sesión
if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None

if choice == "Registro":
    st.subheader("Crear nuevo usuario")
    
    # Formulario de registro
    with st.form("register_form", clear_on_submit=True):
        username = st.text_input("Usuario", help="3-50 caracteres")
        password = st.text_input("Contraseña", type="password", help="Mínimo 6 caracteres")
        role = st.selectbox("Rol", ["user", "admin"], help="Selecciona el rol del usuario")
        submit = st.form_submit_button("Registrar")
        
        if submit:
            if len(username) < 3 or len(username) > 50:
                st.error("El usuario debe tener entre 3 y 50 caracteres")
            elif len(password) < 6:
                st.error("La contraseña debe tener al menos 6 caracteres")
            else:
                data = {"username": username, "password": password, "role": role}
                try:
                    r = requests.post(f"{API_BASE_URL}/register", json=data)
                    if r.status_code == 201:
                        st.success(f"✅ Usuario '{username}' creado correctamente")
                    else:
                        try:
                            error_detail = r.json().get('detail', r.text)
                            st.error(f"❌ Error: {error_detail}")
                        except:
                            st.error(f"❌ Error: {r.text}")
                except Exception as e:
                    st.error(f"❌ Error de conexión: {e}")

if choice == "Login":
    st.subheader("Iniciar sesión")
    
    # Formulario de login
    with st.form("login_form", clear_on_submit=True):
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Entrar")
        
        if submit:
            if not username or not password:
                st.warning("⚠️ Completa usuario y contraseña")
            else:
                data = {"username": username, "password": password}
                try:
                    r = requests.post(f"{API_BASE_URL}/login", json=data)
                    if r.status_code == 200:
                        token = r.json()["access_token"]
                        st.session_state.token = token
                        st.success("✅ Login exitoso")
                        
                        # Obtener datos de usuario
                        headers = {"Authorization": f"Bearer {token}"}
                        r2 = requests.get(f"{API_BASE_URL}/me", headers=headers)
                        if r2.status_code == 200:
                            st.session_state.user = r2.json()
                        else:
                            st.session_state.user = None
                    else:
                        st.error("❌ Credenciales inválidas")
                except Exception as e:
                    st.error(f"❌ Error de conexión: {e}")

    # Mostrar información del usuario logueado
    if st.session_state.token and st.session_state.user:
        # Mostrar información específica según el rol
        if st.session_state.user['role'] == "admin":
            # Probar acceso a ruta de administrador
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            try:
                r = requests.get(f"{API_BASE_URL}/admin", headers=headers)
                if r.status_code == 200:
                    st.success("✅ Acceso confirmado a funciones de administrador")
                else:
                    st.warning("⚠️ No tienes acceso a funciones de administrador")
            except Exception as e:
                st.error(f"❌ Error al verificar acceso: {e}")
        
        # Botón para cerrar sesión
        if st.button("🚪 Cerrar Sesión"):
            st.session_state.token = None
            st.session_state.user = None
            st.success("✅ Sesión cerrada correctamente")
            st.rerun()
