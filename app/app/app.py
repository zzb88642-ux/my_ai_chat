import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Mera AI Chat", page_icon="🤖")
st.title("🤖 Mera AI Chat")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

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
        history = [{"role": c["role"], "parts": c["content"]} 
                   for c in st.session_state.chat_history[:-1]]
        chat = model.start_chat(history=history)
        response = chat.send_message(prompt)
        reply = response.text
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.rerun()

with st.sidebar:
    st.header("ℹ️ Info")
    st.write(f"**Total Messages:** {len(st.session_state.chat_history)}")
