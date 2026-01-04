import streamlit as st
import requests

st.set_page_config(page_title="CAN 2025 Chatbot", page_icon="⚽")
st.title("⚽ CAN 2025 Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des messages
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Posez votre question sur la CAN 2025..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            res = requests.post("http://127.0.0.1:8000/chat", json={"query": prompt})
            if res.status_code == 200:
                answer = res.json().get("response", "Pas de réponse.")
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error("Le serveur ne répond pas.")
        except Exception as e:
            st.error(f"Erreur de connexion : {e}")