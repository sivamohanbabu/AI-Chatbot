import streamlit as st
import ollama

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Ollama Chatbot", layout="wide")
st.title("🤖 Local AI Chatbot (Ollama + Phi-3 / LLMs)")
st.caption("Switch between Normal Mode and 😂 Funny Mode")

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙️ Settings")

    model = st.selectbox("Choose Model", ["phi3", "llama3", "mistral"])
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
    max_tokens = st.slider("Max Tokens", 50, 500, 200)

    funny_mode = st.checkbox("😂 Funny Mode", value=False)

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- DISPLAY CHAT HISTORY ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- USER INPUT ----------------
prompt = st.chat_input("Ask something...")

# ---------------- CHAT LOGIC ----------------
if prompt:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # ---------------- SYSTEM PROMPT (FUNNY / NORMAL MODE) ----------------
    if funny_mode:
        system_prompt = {
            "role": "system",
            "content": (
                "You are a funny, witty, slightly sarcastic AI assistant. "
                "Use jokes, emojis 😄😂, and playful tone while still being correct."
            )
        }
        temperature = min(1.0, temperature + 0.2)  # boost creativity
    else:
        system_prompt = {
            "role": "system",
            "content": "You are a helpful, professional AI assistant."
        }

    # Build final message list
    messages = [system_prompt] + st.session_state.messages

    # ---------------- ASSISTANT RESPONSE ----------------
    with st.chat_message("assistant"):
        placeholder = st.empty()
        response = ""

        stream = ollama.chat(
            model=model,
            messages=messages,
            stream=True,
            options={
                "temperature": temperature,
                "num_predict": max_tokens
            }
        )

        for chunk in stream:
            response += chunk["message"]["content"]
            placeholder.markdown(response)

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("🚀 Built with Streamlit + Ollama | Modes: Normal + Funny 😂")