
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Mera AI Chat", page_icon="🤖")
st.title("🤖 Mera AI Chat")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

col1, col2 = st.columns([4,1])
with col2:
    if st.button("🗑️ Reset"):
        st.session_state.chat_history = []
        st.rerun()

for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])

if prompt := st.chat_input("Sawal likho..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.spinner("Soch raha hai..."):
        model = genai.GenerativeModel("gemini-1.5-flash")
        history = []
        for c in st.session_state.chat_history[:-1]:
            role = "user" if c["role"] == "user" else "model"
            history.append({"role": role, "parts": [c["content"]]})
        chat_session = model.start_chat(history=history)
        response = chat_session.send_message(prompt)
        reply = response.text
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.rerun()

with st.sidebar:
    st.header("ℹ️ Info")
    st.write(f"**Total Messages:** {len(st.session_state.chat_history)}")
