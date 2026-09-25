# import ollama
# import streamlit as st

# st.title("My Streamlit App")

# # 1. Initialize chat history in session state
# if "messages" not in st.session_state:
#   st.session_state.messages = []

# # 2. Display previous chat history on app rerun
# for message in st.session_state.messages:
#   with st.chat_message(message["role"]):
#     st.markdown(message["content"])

# # 3. Get user input
# if prompt := st.chat_input("Type your message here..."):
#   # Display and store user message
#   st.chat_message("user").markdown(prompt)
#   st.session_state.messages.append({"role": "user", "content": prompt})

#   # Call Ollama for response
#   res = ollama.chat(model="llama3", messages=st.session_state.messages)
#   answer = res["message"]["content"]

#   # Display and store assistant response
#   st.chat_message("assistant").markdown(answer)
#   st.session_state.messages.append({"role": "assistant", "content": answer})

# import streamlit as st
# import ollama

# st.set_page_config(page_title="Ollama Phi3 Chatbot", layout="wide")

# st.title("Local AI Chatbot (Phi-3 + Ollama)")

# # Store chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Display previous messages
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# # User input
# prompt = st.chat_input("Ask something...")

# if prompt:
#     # Save user message
#     st.session_state.messages.append({"role": "as a developer,write only code", "content": prompt})

#     with st.chat_message("user"):
#         st.markdown(prompt)

#     # Assistant response (streaming)
#     with st.chat_message("assistant"):
#         placeholder = st.empty()
#         response_text = ""

#         stream = ollama.chat(
#             model="phi3",
#             messages=st.session_state.messages,
#             stream=True,
#             options={
#                 "num_predict": 200,   # limit tokens for speed
#                 "temperature": 0.7
#             }
#         )

#         for chunk in stream:
#             content = chunk["message"]["content"]
#             response_text += content
#             placeholder.markdown(response_text)

#         # Save assistant response
#         st.session_state.messages.append(
#             {"role": "assistant", "content": response_text}
#         )

import streamlit as st
import ollama

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Phi3 Chatbot", layout="wide")
st.title("Local AI Chatbot (Ollama + Phi-3)")

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙️ Settings")

    model = st.selectbox("Choose Model", ["phi3", "llama3", "mistral"])
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
    max_tokens = st.slider("Max Tokens", 50, 500, 200)

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
    # user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # assistant response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        response = ""

        stream = ollama.chat(
            model=model,
            messages=st.session_state.messages,
            stream=True,
            options={
                "temperature": temperature,
                "num_predict": max_tokens
            }
        )

        for chunk in stream:
            response += chunk["message"]["content"]
            placeholder.markdown(response)

    # save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

# ---------------- FOOTER ----------------
st.caption("🚀 Powered by Streamlit + Ollama (Phi-3 / LLMs)")