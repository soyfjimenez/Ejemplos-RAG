import streamlit as st
from core.react_agent import ProcessUserInput
import os
import time
st.set_page_config(page_title="Mi primer RAG", page_icon="💬")




import os
import time

# Sidebar: Archivos generados
st.sidebar.title("📁 Archivos generados")

folder_path = "generated_files"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

if files:
    with st.sidebar.container():
        for filename in files:
            filepath = os.path.join(folder_path, filename)
            creation_time = time.strftime("%d %b %Y %H:%M", time.localtime(os.path.getctime(filepath)))

            # Contenedor individual para cada archivo
            with st.sidebar.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                # Línea superior: nombre y fecha
                with col1:
                    st.markdown(f"**📝 {filename}**")
                    st.markdown(f"<span style='font-size: 12px; color: gray;'>🕒 {creation_time}</span>", unsafe_allow_html=True)

                # Botones de acción

                with open(filepath, "rb") as file_data:
                    col2.download_button(
                        label="📥",
                        data=file_data,
                        file_name=filename,
                        key=f"download_{filename}",
                        help="Descargar archivo"
                    )

                if col3.button("🗑️", key=f"delete_{filename}", help="Eliminar archivo"):
                    os.remove(filepath)
                    st.rerun()

                st.markdown("---")  # Separador entre archivos
else:
    st.sidebar.info("No hay archivos generados aún.")





st.header('Mi primer Agentic RAG')

# Initialize session state for messages and default parameters
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'temperature' not in st.session_state:
    st.session_state.temperature = 0.7
if 'top_k' not in st.session_state:
    st.session_state.top_k = 3
if 'similarity_threshold' not in st.session_state:
    st.session_state.similarity_threshold = 0.5

# Parámetros en tres columnas
col1, col2, col3 = st.columns(3)

with col1:
    st.session_state.temperature = col1.slider(
        "Temperatura (creatividad)",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.temperature,
        step=0.1,
    )

with col2:
    st.session_state.top_k = col2.slider(
        "Top-k",
        min_value=1,
        max_value=10,
        value=st.session_state.top_k,
        step=1,
    )

with col3:
    st.session_state.similarity_threshold = col3.slider(
        "Umbral de similaridad",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.similarity_threshold,
        step=0.10,
    )

def main():
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.write(message['content'])

    # Accept user input
    if user_input := st.chat_input("Escribe tu mensaje..."):
        # Display user message in chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Process user input using the ProcessUserInput function
        response_data = ProcessUserInput(
            user_input,
            temperature=st.session_state.temperature
        )

        # Extract response and documents
        response = response_data.get("response", "No response available.")
        # Display LLM-generated response
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)
        st.rerun()

if __name__ == "__main__":
    main()