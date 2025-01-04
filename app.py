import openai
import streamlit as st

# Streamlit app title
st.title("CJ Bot")

# Set OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Initialize session state for OpenAI model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("What is up?"):
    # Add user message to session state
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    response_content = ""
    with st.chat_message("assistant"):
        response_placeholder = st.empty()  # Placeholder for streaming content
        for chunk in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=st.session_state["messages"],
            stream=True,
        ):
            # Extract content from streamed chunk
            content = chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")
            response_content += content
            response_placeholder.markdown(response_content)  # Update placeholder

    # Add assistant response to session state
    st.session_state["messages"].append({"role": "assistant", "content": response_content})
