import streamlit as st
from chatbot import ask_egosa

st.set_page_config(page_title="Egosa", page_icon="⚽")

with st.sidebar:
    st.header("About Egosa")
    st.write("A football-only chatbot covering:")
    st.write("⚽ La Liga")
    st.write("⚽ Premier League")
    st.write("⚽ Champions League")
    st.divider()
    st.caption("Built with RAG: FAISS + sentence-transformers + Gemini")

st.title("⚽ Egosa")
st.caption("Ask me about La Liga, Premier League, or Champions League")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    avatar = "🧑" if message["role"] == "user" else "⚽"
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])

user_input = None

if not st.session_state.messages:
    st.write("Try asking:")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Most La Liga titles?"):
            user_input = "who won the most la liga titles"
    with col2:
        if st.button("Top CL scorer?"):
            user_input = "who is the top scorer in champions league history"
    with col3:
        if st.button("Premier League records?"):
            user_input = "premier league goal record"

typed_input = st.chat_input("Ask Egosa a question...")
if typed_input:
    user_input = typed_input

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑"):
        st.write(user_input)

    answer = ask_egosa(user_input)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant", avatar="⚽"):
        st.write(answer)

    if len(st.session_state.messages) == 2:
        st.rerun()