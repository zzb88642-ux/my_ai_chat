import streamlit as st
from groq import Groq

st.set_page_config(page_title="Mera AI Chat", page_icon="🤖")
st.title("🤖 Mera AI Chat")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

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
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=st.session_state.chat_history
        )
        reply = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.rerun()

with st.sidebar:
    st.header("ℹ️ Info")
    st.write(f"**Total Messages:** {len(st.session_state.chat_history)}")
