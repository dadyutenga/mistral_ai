import json
import os
import requests
import streamlit as st

# Mistral API Configuration
os.environ["MISTRAL_API_KEY"] = "tSFznebT56lFfbCt9i5NQzCHcsEUEGAf" #TODO: Insert Mistral API key
api_key = os.environ["MISTRAL_API_KEY"]

def get_mistral_response(question):
    """Get response from Mistral API"""
    output = {
        "prefix": "A description of the code solution",
        "programming_language": "The programming language",
        "imports": "The imports",
        "code": "The functioning code block",
        "sample_io": "Generate the sample input and output for the code generated {'input': '', 'output': ''}"
    }

    messages = [{
        "role": "system",
        "content": f"""You're a coding assistant. Ensure any code you provided can be executed with all required imports and variables defined.
        Structure your answer in the JSON format: {output}

        Here's the question: """
    }, {"role": "user", "content": question}]

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    res = requests.post(
        "https://codestral.mistral.ai/v1/chat/completions",
        headers=headers,
        json={
            "model": "codestral-latest",
            "messages": messages,
            "response_format": {"type": "json_object"}
        }
    )
    
    response = res.json()["choices"][0]["message"]["content"]
    response = response.replace("```python", "").replace("```", "")
    return json.loads(response)

# Configure the page
st.set_page_config(
    page_title="CoderChat",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme and styling
st.markdown("""
<style>
    /* Dark theme */
    .stApp {
        background-color: #1A1A1A;
        color: white;
    }
    
    /* Top navigation bar */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2rem;
        background-color: #1A1A1A;
        border-bottom: 1px solid #2D2D2D;
    }
    
    .logo {
        font-size: 1.5rem;
        font-weight: bold;
    }
    
    .profile-icon {
        width: 35px;
        height: 35px;
        background-color: white;
        border-radius: 50%;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        max-width: 60%;
        line-height: 1.4;
    }
    
    .assistant-message {
        background-color: #2D2D2D;
        margin-left: 2rem;
        float: left;
    }
    
    .user-message {
        background-color: #0D6EFD;
        margin-right: 2rem;
        float: right;
    }
    
    /* Code block styling */
    .code-block {
        background-color: #2D2D2D;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    /* Input area styling */
    .input-area {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 1rem 2rem;
        background-color: #1A1A1A;
        display: flex;
        gap: 0.5rem;
        align-items: center;
    }
    
    .input-button {
        background-color: #2D2D2D;
        border: none;
        border-radius: 8px;
        padding: 0.5rem;
        cursor: pointer;
        color: white;
    }
    
    .send-button {
        background-color: #0D6EFD;
    }
    
    .message-input {
        flex-grow: 1;
        background-color: #2D2D2D;
        border: none;
        border-radius: 8px;
        padding: 0.8rem;
        color: white;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
</style>

<div class="top-nav">
    <div class="logo">CoderChat</div>
    <div class="profile-icon"></div>
</div>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 style='text-align: center; font-size: 2.5rem; margin-top: 2rem;'>Welcome to CoderChat</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #808080;'>Your AI coding assistant is ready to help!</p>", unsafe_allow_html=True)

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I assist you with your coding questions today?"}
    ]

# Display chat messages and handle input
if "messages" in st.session_state:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "user":
                st.markdown(f"""<div class='chat-message user-message'>{message["content"]}</div>""", unsafe_allow_html=True)
            else:
                if isinstance(message["content"], dict):
                    # Display structured response
                    if message["content"].get("prefix"):
                        st.write("Description:")
                        st.write(message["content"]["prefix"])
                    if message["content"].get("imports"):
                        st.write("Imports:")
                        st.code(message["content"]["imports"], language=message["content"]["programming_language"])
                    if message["content"].get("code"):
                        st.write("Code:")
                        st.code(message["content"]["code"], language=message["content"]["programming_language"])
                    if message["content"].get("sample_io"):
                        if message["content"]["sample_io"].get("input"):
                            st.write("Sample Input:")
                            st.code(message["content"]["sample_io"]["input"], language=message["content"]["programming_language"])
                        if message["content"]["sample_io"].get("output"):
                            st.write("Sample Output:")
                            st.code(message["content"]["sample_io"]["output"], language=message["content"]["programming_language"])
                else:
                    st.markdown(f"""<div class='chat-message assistant-message'>{message["content"]}</div>""", unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"""<div class='chat-message user-message'>{prompt}</div>""", unsafe_allow_html=True)
    
    # Get AI response
    with st.chat_message("assistant"):
        response = get_mistral_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Display structured response
        if response.get("prefix"):
            st.write("Description:")
            st.write(response["prefix"])
        if response.get("imports"):
            st.write("Imports:")
            st.code(response["imports"], language=response["programming_language"])
        if response.get("code"):
            st.write("Code:")
            st.code(response["code"], language=response["programming_language"])
        if response.get("sample_io"):
            if response["sample_io"].get("input"):
                st.write("Sample Input:")
                st.code(response["sample_io"]["input"], language=response["programming_language"])
            if response["sample_io"].get("output"):
                st.write("Sample Output:")
                st.code(response["sample_io"]["output"], language=response["programming_language"])