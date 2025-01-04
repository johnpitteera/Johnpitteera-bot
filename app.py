import openai
import streamlit as st

# Streamlit app title
st.title("CJ Bot")

# Attempt to set the OpenAI API key
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("The OpenAI API key is missing. Please add it to `.streamlit/secrets.toml` or Streamlit Cloud secrets.")
    st.stop()  # Stop the app if the API key is not found

# Initialize session state for the OpenAI model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize session state for chat messages
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("What is up?"):
    # Add user input to session state
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    response_content = ""
    with st.chat_message("assistant"):
        response_placeholder = st.empty()  # Placeholder for the response
        for chunk in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=st.session_state["messages"],
            stream=True,
        ):
            # Extract content from each streamed chunk
            content = chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")
            response_content += content
            response_placeholder.markdown(response_content)  # Update placeholder with the streamed content

    # Add the assistant's response to session state
    st.session_state["messages"].append({"role": "assistant", "content": response_content})
