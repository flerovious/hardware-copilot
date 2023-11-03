import openai
import streamlit as st

st.title("Hardware Copilot")

openai.api_key = st.secrets["OPENAI_API_KEY"]

initial_prompt = """
I am working a hardware project, implementing it on an arduino uno. 
I need help with wiring and writing out the full code. Tell me what are 
the sensors and ports I'll need to connect together with the arduino code 
I'll need to write. Write some test code where possible. Here are my 
requirements:

Format the output to be in the following format:
- Hardware required:
- Wiring:
- Arduino code:
- Additional notes:
"""

if not st.session_state.get("messages"):
    st.caption("What would you like to build today?")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(""):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {
                    "role": m["role"],
                    "content": m["content"]
                    if i != 0
                    else initial_prompt + m["content"],
                }
                for i, m in enumerate(st.session_state.messages)
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
