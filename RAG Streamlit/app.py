import streamlit as st
from core.react_agent import ProcessUserInput

st.set_page_config(page_title="Mi primer RAG", page_icon="💬")
st.header('Mi primer Agentic RAG')

# Initialize session state for messages and default parameters
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'temperature' not in st.session_state:
    st.session_state.temperature = 0.7
if 'top_k' not in st.session_state:
    st.session_state.top_k = 3
if 'threshold' not in st.session_state:
    st.session_state.threshold = 0.5

# Parámetros en columnas
col1 = st.columns(1)[0]

with col1:
    st.session_state.temperature = col1.slider(
        "Temperatura (creatividad)",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.temperature,
        step=0.1,
    )

def main():
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.write(message['content'])

    # Accept user input
    if user_input := st.chat_input("Type your message..."):
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

if __name__ == "__main__":
    main()