import json
import os
import requests
import streamlit as st
import base64
from pathlib import Path

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

def handle_file_upload():
    uploaded_file = st.file_uploader("Choose a file", type=['py', 'js', 'java', 'cpp', 'txt', 'json', 'html', 'css'], key="file_uploader")
    if uploaded_file is not None:
        file_contents = uploaded_file.read()
        if isinstance(file_contents, bytes):
            file_contents = file_contents.decode('utf-8')
        
        file_extension = Path(uploaded_file.name).suffix.lower()[1:]
        
        st.session_state.messages.append({
            "role": "user", 
            "content": f"I have uploaded a {file_extension} file with the following contents:\n```{file_extension}\n{file_contents}\n```"
        })
        
        st.session_state.show_uploader = False
        st.rerun()

# Configure the page
st.set_page_config(
    page_title="CoderChat",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I assist you with your coding questions today?"}
    ]

if 'show_uploader' not in st.session_state:
    st.session_state.show_uploader = False

# Update the CSS to match the exact design
st.markdown("""
<style>
    /* Dark theme */
    .stApp {
        background-color: #1A1A1A !important;
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
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
    }
    
    .logo {
        font-size: 1.5rem;
        font-weight: 500;
        color: white;
    }
    
    .profile-icon {
        width: 32px;
        height: 32px;
        background-color: white;
        border-radius: 50%;
    }
    
    /* Chat container */
    .chat-container {
        margin-top: 80px;
        padding: 20px;
        max-width: 1200px;
        margin-left: auto;
        margin-right: auto;
        margin-bottom: 120px;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1rem 1.5rem;
        border-radius: 20px;
        margin: 1rem 0;
        max-width: 70%;
        line-height: 1.5;
        font-size: 16px;
    }
    
    .assistant-message {
        background-color: #2D2D2D;
        margin-left: 0;
        float: left;
        clear: both;
    }
    
    .user-message {
        background-color: #0D6EFD;
        float: right;
        clear: both;
    }
    
    /* Code block styling */
    .code-block {
        background-color: #2D2D2D;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    /* Input area styling */
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 1.5rem 2rem;
        background-color: #1A1A1A;
        border-top: 1px solid #2D2D2D;
    }
    
    .input-group {
        display: flex;
        gap: 0.75rem;
        max-width: 1200px;
        margin: 0 auto;
        align-items: center;
    }
    
    .input-button {
        background-color: #2D2D2D;
        border: none;
        border-radius: 8px;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        color: #808080;
    }
    
    .send-button {
        background-color: #0D6EFD;
        color: white;
    }
    
    .message-input {
        flex-grow: 1;
        background-color: #2D2D2D;
        border: none;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        color: white;
        font-size: 16px;
    }
    
    /* Welcome message styling */
    .welcome-title {
        font-size: 2.5rem;
        font-weight: 600;
        text-align: center;
        margin-top: 3rem;
        margin-bottom: 1rem;
    }
    
    .welcome-subtitle {
        text-align: center;
        color: #808080;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    .st-emotion-cache-1y4p8pa {padding-top: 0 !important;}
    .st-emotion-cache-1544g2n {padding-top: 0 !important;}
    
    /* Adjust padding for chat messages */
    .stMarkdown {margin-top: 0 !important;}
    
    /* File uploader styling */
    .upload-container {
        position: fixed;
        bottom: 100px;
        left: 50%;
        transform: translateX(-50%);
        background-color: #2D2D2D;
        padding: 1rem;
        border-radius: 8px;
        z-index: 1000;
        width: 90%;
        max-width: 600px;
    }
    
    .stFileUploader {
        margin-bottom: 0 !important;
    }
    
    .uploadButton:hover {
        border-color: #0D6EFD !important;
    }
    
    /* Hide the attachment button */
    [data-testid="stButton"] {
        display: none;
    }
    
    /* Show the custom attachment button */
    .input-button {
        display: flex;
    }
    
    /* Code response styling */
    .code-response {
        background-color: #2D2D2D;
        border-radius: 12px;
        padding: 20px;
        width: 90%;
        max-width: 800px;
    }
    
    .response-section {
        margin-bottom: 20px;
    }
    
    .section-title {
        color: #0D6EFD;
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 10px;
    }
    
    .section-content {
        color: #E0E0E0;
        line-height: 1.5;
    }
    
    .description-content {
        background-color: #363636;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    
    .io-section {
        margin-top: 10px;
    }
    
    .io-label {
        color: #808080;
        font-size: 0.9rem;
        margin-bottom: 5px;
    }
    
    /* Code block styling */
    .stCodeBlock {
        background-color: #363636 !important;
        border-radius: 8px !important;
        margin-bottom: 15px !important;
    }
    
    .stCodeBlock > div {
        background-color: transparent !important;
    }
    
    /* Syntax highlighting colors */
    .language-python {
        color: #E0E0E0;
    }
    
    .keyword {
        color: #0D6EFD;
    }
    
    .string {
        color: #98C379;
    }
    
    .number {
        color: #D19A66;
    }
    
    .comment {
        color: #808080;
    }
</style>

<div class="top-nav">
    <div class="logo">CoderChat</div>
    <div class="profile-icon"></div>
</div>

<div class="chat-container">
    <div class="welcome-title">Welcome to CoderChat</div>
    <div class="welcome-subtitle">Your AI coding assistant is ready to help!</div>
</div>
""", unsafe_allow_html=True)

# Add to session state initialization
if 'show_uploader' not in st.session_state:
    st.session_state.show_uploader = False

# Add file upload container before the input container
if st.session_state.show_uploader:
    with st.container():
        st.markdown('<div class="upload-container">', unsafe_allow_html=True)
        handle_file_upload()
        st.markdown('</div>', unsafe_allow_html=True)

# Update the input container HTML to include click handler for attachment button
st.markdown("""
<div class="input-container">
    <div class="input-group">
        <button class="input-button" onclick="toggleUploader()">📎</button>
        <button class="input-button">🎤</button>
        <input type="text" class="message-input" placeholder="Type your message...">
        <button class="input-button send-button">➤</button>
    </div>
</div>
""", unsafe_allow_html=True)

# Add JavaScript to handle the attachment button click
st.markdown("""
<script>
function toggleUploader() {
    // Toggle the uploader state
    const value = true;  // We'll handle the toggle in Python
    window.parent.postMessage({
        type: 'streamlit:setComponentValue',
        value: value
    }, '*');
}
</script>
""", unsafe_allow_html=True)

# Display chat messages and handle input
if "messages" in st.session_state:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""<div class='chat-message user-message'>{message["content"]}</div>""", unsafe_allow_html=True)
        else:
            if isinstance(message["content"], dict):
                st.markdown("""
                <div class='chat-message assistant-message code-response'>
                """, unsafe_allow_html=True)
                
                # Description
                if message["content"].get("prefix"):
                    st.markdown("""
                    <div class='response-section'>
                        <div class='section-title'>Description</div>
                        <div class='section-content description-content'>
                            {}
                        </div>
                    </div>
                    """.format(message["content"]["prefix"]), unsafe_allow_html=True)
                
                # Code Implementation
                if message["content"].get("code"):
                    st.markdown("""
                    <div class='response-section'>
                        <div class='section-title'>Implementation</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Imports
                    if message["content"].get("imports"):
                        st.code(message["content"]["imports"], 
                               language=message["content"]["programming_language"])
                    
                    # Main Code
                    st.code(message["content"]["code"], 
                           language=message["content"]["programming_language"])
                
                # Sample Input/Output
                if message["content"].get("sample_io"):
                    st.markdown("""
                    <div class='response-section'>
                        <div class='section-title'>Example Usage</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if message["content"]["sample_io"].get("input"):
                        st.markdown("""
                        <div class='io-section'>
                            <div class='io-label'>Input:</div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.code(message["content"]["sample_io"]["input"], 
                               language=message["content"]["programming_language"])
                    
                    if message["content"]["sample_io"].get("output"):
                        st.markdown("""
                        <div class='io-section'>
                            <div class='io-label'>Output:</div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.code(message["content"]["sample_io"]["output"], 
                               language=message["content"]["programming_language"])
                
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div class='chat-message assistant-message'>{message["content"]}</div>""", 
                          unsafe_allow_html=True)

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