import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Formulario de Contacto", page_icon="✉️")

# Título de la aplicación
st.title("Formulario de Contacto")

# Descripción
st.write("Por favor, completa el formulario a continuación y haz clic en 'Enviar'.")

# Formulario de contacto
with st.form("contact_form"):
    name = st.text_input("Nombre completo", placeholder="Ingresa tu nombre")
    email = st.text_input("Correo electrónico", placeholder="Ingresa tu correo electrónico")
    message = st.text_area("Mensaje", placeholder="Escribe tu mensaje aquí...")

    # Botón de envío
    submitted = st.form_submit_button("Enviar")

# Manejo de envío del formulario
if submitted:
    if not name or not email or not message:
        st.error("Por favor, completa todos los campos.")
    else:
        st.success("¡Gracias por tu mensaje! Nos pondremos en contacto contigo pronto.")
        st.write("### Información enviada:")
        st.write(f"- **Nombre:** {name}")
        st.write(f"- **Correo:** {email}")
        st.write(f"- **Mensaje:** {message}")