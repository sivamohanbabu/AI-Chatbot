import streamlit as st
import ollama

st.title("AI Chatbot")



selected_model = st.selectbox("Model", ["phi3", "llama3", "mistral"])
temperature_value = st.slider("Temperature", 0.0, 1.0, 0.7)

user_prompt = st.chat_input("Ask something...")

if user_prompt:
    with st.chat_message("user"):
        st.write(user_prompt)

    with st.chat_message("assistant"):
        response_text = ""
        output_box = st.empty()

        for chunk in ollama.chat(
            model=selected_model,
            messages=[{"role": "user", "content": user_prompt}],
            stream=True,
            options={"temperature": temperature_value}
        ):
            response_text += chunk["message"]["content"]
            output_box.markdown(response_text)