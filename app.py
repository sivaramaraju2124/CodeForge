import streamlit as st
from streamlit_ace import st_ace
import requests
import time
import openai
from PIL import Image
import base64
import io
from groq import Groq
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
import pyperclip
import sqlite3

# -------- Groq API Setup --------
openai.api_key = "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"
openai.base_url = "https://api.groq.com/openai/v1"
client = Groq(api_key=openai.api_key)

# -------- Judge0 Setup --------
JUDGE0_URL = "https://judge0-ce.p.rapidapi.com/submissions"
JUDGE0_HEADERS = {
    "Content-Type": "application/json",
    "X-RapidAPI-Key": "dfe8e4a385mshf85714d2765af5ep1ea212jsnbc9eee191709",
    "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com"
}

judge0_language_ids = {
    "python": 71,
    "javascript": 63,
    "java": 62,
    "c_cpp": 54,
    "bash": 46
}

# CSS for theme styling
def load_css(theme_mode="dark"):
    if theme_mode == "dark":
        st.markdown("""
        <style>
            /* Splash Screen Styling */
            .splash-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                width: 100%;
                background-color: #1e1e2e;  /* Dark theme background */
                position: fixed;
                top: 0;
                left: 0;
                z-index: 9999;
            }

            .splash-logo {
                margin-bottom: 2rem;
                animation: fadeInDown 1.5s ease-out;
            }

            .splash-title {
                color: #bd93f9;
                font-size: 2.5rem;
                margin-bottom: 1rem;
                animation: fadeInUp 1.5s ease-out;
            }

            .splash-subtitle {
                color: #f8f8f2;
                font-size: 1.2rem;
                margin-bottom: 2rem;
                animation: fadeInUp 1.8s ease-out;
            }

            .splash-progress {
                width: 80%;
                max-width: 400px;
                animation: fadeIn 2s ease-out;
            }

            /* Splash screen animations */
            @keyframes fadeInDown {
                0% {
                    opacity: 0;
                    transform: translateY(-30px);
                }
                100% {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            @keyframes fadeInUp {
                0% {
                    opacity: 0;
                    transform: translateY(30px);
                }
                100% {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            @keyframes fadeIn {
                0% { opacity: 0; }
                100% { opacity: 1; }
            }
            /* Dark Theme */
            .main {
                background-color: #1e1e2e;
                color: #f8f8f2;
            }
            
            /* Custom Header */
            .stApp header {
                background-color: #282a36;
                border-bottom: 1px solid #44475a;
            }
            
            /* Custom Title */
            h1, h2, h3 {
                color: #bd93f9 !important;
                font-weight: 600 !important;
            }
            
            /* Custom Buttons */
            .stButton>button {
                background-color: #6272a4;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 0.5rem 1rem;
                font-weight: 500;
                transition: all 0.3s;
            }
            
            .stButton>button:hover {
                background-color: #44475a;
                transform: translateY(-2px);
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            
            /* Run Button Special Styling */
            .run-btn>button {
                background-color: #50fa7b !important;
                color: #282a36 !important;
                font-weight: 600 !important;
                padding: 0.5rem 1.5rem !important;
            }
            
            .run-btn>button:hover {
                background-color: #5af78e !important;
            }
            
            /* Nav Styling */
            .nav-link {
                border-radius: 5px !important;
                margin: 0.2rem 0 !important;
                font-weight: 500 !important;
            }
            
            .nav-link.active {
                background-color: #bd93f9 !important;
                color: #282a36 !important;
            }
            
            /* Card Styling */
            .css-1r6slb0 {
                border: 1px solid #44475a !important;
                border-radius: 8px !important;
                padding: 1.5rem !important;
                background-color: #282a36 !important;
                margin-bottom: 1.5rem !important;
            }
            
            /* Info box styling */
            .stAlert {
                background-color: #44475a !important;
                color: #f8f8f2 !important;
                border: none !important;
                border-radius: 4px !important;
            }
            
            /* Sidebar */
            .css-1d391kg {
                background-color: #282a36 !important;
            }
            
            /* Text Areas */
            .stTextArea textarea {
                background-color: #282a36 !important;
                color: #f8f8f2 !important;
                border: 1px solid #44475a !important;
                border-radius: 4px !important;
            }
            
            /* Progress Bars */
            .stProgress > div > div {
                background-color: #bd93f9 !important;
            }
            
            /* File Uploader */
            .uploadedFileData {
                background-color: #44475a !important;
                border: 1px solid #6272a4 !important;
                border-radius: 5px !important;
                padding: 1rem !important;
            }
            
            /* Tool Tips */
            .stTooltipIcon {
                color: #6272a4 !important;
            }
            
            /* Section Dividers */
            hr {
                border-color: #44475a !important;
                margin: 2rem 0 !important;
            }
            
            /* Icons */
            .icon-text {
                display: inline-flex;
                align-items: center;
                gap: 5px;
            }
            
            /* Animation */
            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.6; }
                100% { opacity: 1; }
            }
            
            .pulse {
                animation: pulse 2s infinite;
            }
            
            /* Tabs */
            .stTabs [data-baseweb="tab-list"] {
                gap: 2px;
                background-color: #282a36;
            }
            
            .stTabs [data-baseweb="tab"] {
                background-color: #44475a;
                color: #f8f8f2;
                border-radius: 4px 4px 0 0;
                padding: 10px 20px;
                font-size: 14px;
            }
            
            .stTabs [aria-selected="true"] {
                background-color: #bd93f9;
                color: #282a36;
                font-weight: bold;
            }
            
            /* Chat container styling - limiting width */
            .chat-container {
                background-color: #282a36;
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
                margin: 20px auto;
                border: 1px solid #44475a;
                max-width: 600px; /* Limit the width */
                width: 90%; /* Responsive width */
            }
            
            /* Message container */
            .message-container {
                display: flex;
                margin-bottom: 12px;
                flex-direction: column;
            }
            
            /* User message styling */
            .user-msg {
                background-color: #6272a4;
                color: white;
                border-radius: 12px 12px 0 12px;
                padding: 10px 15px;
                margin: 5px 0;
                max-width: 80%;
                align-self: flex-end;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                margin-left: auto;
                word-wrap: break-word;
            }
            
            /* Bot message styling */
            .bot-msg {
                background-color: #44475a;
                color: #f8f8f2;
                border-radius: 12px 12px 12px 0;
                padding: 10px 15px;
                margin: 5px 0;
                max-width: 80%;
                align-self: flex-start;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                margin-right: auto;
                word-wrap: break-word;
            }
            
            /* Sender name styling */
            .sender-name {
                font-weight: 600;
                margin-bottom: 3px;
                font-size: 0.9em;
                opacity: 0.8;
            }
            
            /* Chat header styling */
            .chat-header {
                display: flex;
                align-items: center;
                margin-bottom: 15px;
                padding-bottom: 10px;
                border-bottom: 1px solid #44475a;
            }
            
            .chat-header h3 {
                margin: 0;
                color: #bd93f9;
            }
            
            /* Chat input container */
            .chat-input-container {
                display: flex;
                flex-direction: column;
                gap: 8px;
                margin-top: 15px;
            }
            
            /* Streamlit specific overrides for chatbot */
            .stButton > button.chat-send-btn {
                background-color: #6272a4 !important;
                color: white !important;
                border-radius: 20px !important;
                padding: 0.3rem 1.5rem !important;
                font-size: 14px !important;
                font-weight: 500 !important;
                border: none !important;
                cursor: pointer !important;
                transition: all 0.3s ease !important;
            }
            
            .stButton > button.chat-send-btn:hover {
                background-color: #bd93f9 !important;
                transform: translateY(-2px) !important;
            }
            
            /* Ensure the chat appears in center of its container */
            .chat-wrapper {
                display: flex;
                justify-content: center;
                width: 100%;
            }
            
            /* Theme toggle button */
            .theme-toggle {
                cursor: pointer;
                background-color: #44475a;
                color: #f8f8f2;
                border: none;
                border-radius: 15px;
                padding: 5px 15px;
                font-size: 14px;
                transition: all 0.3s;
                display: flex;
                align-items: center;
                gap: 5px;
            }
            
            .theme-toggle:hover {
                background-color: #6272a4;
            }
            
            /* Linting error markers */
            .ace_error {
                background-color: rgba(255, 100, 100, 0.2);
                position: absolute;
                z-index: 5;
            }
            
            .ace_error-marker {
                background-color: rgba(255, 100, 100, 0.4);
                position: absolute;
            }
            
            .ace_warning {
                background-color: rgba(255, 165, 0, 0.2);
                position: absolute;
                z-index: 5;
            }
            
            .ace_lint-tooltip {
                background-color: #282a36;
                border: 1px solid #44475a;
                color: #f8f8f2;
                padding: 5px 10px;
                border-radius: 4px;
                font-size: 12px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
            }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            /* Light Theme */
            .main {
                background-color: #f8f9fa;
                color: #212529;
            }
            
            /* Custom Header */
            .stApp header {
                background-color: #ffffff;
                border-bottom: 1px solid #dee2e6;
            }
            
            /* Custom Title */
            h1, h2, h3 {
                color: #3949ab !important;
                font-weight: 600 !important;
            }
            
            /* Custom Buttons */
            .stButton>button {
                background-color: #3949ab;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 0.5rem 1rem;
                font-weight: 500;
                transition: all 0.3s;
            }
            
            .stButton>button:hover {
                background-color: #283593;
                transform: translateY(-2px);
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            
            /* Run Button Special Styling */
            .run-btn>button {
                background-color: #4caf50 !important;
                color: white !important;
                font-weight: 600 !important;
                padding: 0.5rem 1.5rem !important;
            }
            
            .run-btn>button:hover {
                background-color: #43a047 !important;
            }
            
            /* Nav Styling */
            .nav-link {
                border-radius: 5px !important;
                margin: 0.2rem 0 !important;
                font-weight: 500 !important;
            }
            
            .nav-link.active {
                background-color: #3949ab !important;
                color: white !important;
            }
            
            /* Card Styling */
            .css-1r6slb0 {
                border: 1px solid #dee2e6 !important;
                border-radius: 8px !important;
                padding: 1.5rem !important;
                background-color: #ffffff !important;
                margin-bottom: 1.5rem !important;
            }
            
            /* Info box styling */
            .stAlert {
                background-color: #e9ecef !important;
                color: #212529 !important;
                border: none !important;
                border-radius: 4px !important;
            }
            
            /* Sidebar */
            .css-1d391kg {
                background-color: #f8f9fa !important;
            }
            
            /* Text Areas */
            .stTextArea textarea {
                background-color: #ffffff !important;
                color: #212529 !important;
                border: 1px solid #ced4da !important;
                border-radius: 4px !important;
            }
            
            /* Progress Bars */
            .stProgress > div > div {
                background-color: #3949ab !important;
            }
            
            /* File Uploader */
            .uploadedFileData {
                background-color: #e9ecef !important;
                border: 1px solid #ced4da !important;
                border-radius: 5px !important;
                padding: 1rem !important;
            }
            
            /* Tool Tips */
            .stTooltipIcon {
                color: #6c757d !important;
            }
            
            /* Section Dividers */
            hr {
                border-color: #dee2e6 !important;
                margin: 2rem 0 !important;
            }
            
            /* Icons */
            .icon-text {
                display: inline-flex;
                align-items: center;
                gap: 5px;
            }
            
            /* Animation */
            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.6; }
                100% { opacity: 1; }
            }
            
            .pulse {
                animation: pulse 2s infinite;
            }
            
            /* Tabs */
            .stTabs [data-baseweb="tab-list"] {
                gap: 2px;
                background-color: #f8f9fa;
            }
            
            .stTabs [data-baseweb="tab"] {
                background-color: #e9ecef;
                color: #212529;
                border-radius: 4px 4px 0 0;
                padding: 10px 20px;
                font-size: 14px;
            }
            
            .stTabs [aria-selected="true"] {
                background-color: #3949ab;
                color: white;
                font-weight: bold;
            }
            
            /* Chat container styling - limiting width */
            .chat-container {
                background-color: #ffffff;
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                margin: 20px auto;
                border: 1px solid #dee2e6;
                max-width: 600px; /* Limit the width */
                width: 90%; /* Responsive width */
            }
            
            /* Message container */
            .message-container {
                display: flex;
                margin-bottom: 12px;
                flex-direction: column;
            }
            
            /* User message styling */
            .user-msg {
                background-color: #3949ab;
                color: white;
                border-radius: 12px 12px 0 12px;
                padding: 10px 15px;
                margin: 5px 0;
                max-width: 80%;
                align-self: flex-end;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                margin-left: auto;
                word-wrap: break-word;
            }
            
            /* Bot message styling */
            .bot-msg {
                background-color: #e9ecef;
                color: #212529;
                border-radius: 12px 12px 12px 0;
                padding: 10px 15px;
                margin: 5px 0;
                max-width: 80%;
                align-self: flex-start;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                margin-right: auto;
                word-wrap: break-word;
            }
            
            /* Sender name styling */
            .sender-name {
                font-weight: 600;
                margin-bottom: 3px;
                font-size: 0.9em;
                opacity: 0.8;
            }
            
            /* Chat header styling */
            .chat-header {
                display: flex;
                align-items: center;
                margin-bottom: 15px;
                padding-bottom: 10px;
                border-bottom: 1px solid #dee2e6;
            }
            
            .chat-header h3 {
                margin: 0;
                color: #3949ab;
            }
            
            /* Chat input container */
            .chat-input-container {
                display: flex;
                flex-direction: column;
                gap: 8px;
                margin-top: 15px;
            }
            
            /* Streamlit specific overrides for chatbot */
            .stButton > button.chat-send-btn {
                background-color: #3949ab !important;
                color: white !important;
                border-radius: 20px !important;
                padding: 0.3rem 1.5rem !important;
                font-size: 14px !important;
                font-weight: 500 !important;
                border: none !important;
                cursor: pointer !important;
                transition: all 0.3s ease !important;
            }
            
            .stButton > button.chat-send-btn:hover {
                background-color: #283593 !important;
                transform: translateY(-2px) !important;
            }
            
            /* Ensure the chat appears in center of its container */
            .chat-wrapper {
                display: flex;
                justify-content: center;
                width: 100%;
            }
            
            /* Theme toggle button */
            .theme-toggle {
                cursor: pointer;
                background-color: #e9ecef;
                color: #212529;
                border: none;
                border-radius: 15px;
                padding: 5px 15px;
                font-size: 14px;
                transition: all 0.3s;
                display: flex;
                align-items: center;
                gap: 5px;
            }
            
            .theme-toggle:hover {
                background-color: #ced4da;
            }
            
            /* Linting error markers */
            .ace_error {
                background-color: rgba(255, 100, 100, 0.2);
                position: absolute;
                z-index: 5;
            }
            
            .ace_error-marker {
                background-color: rgba(255, 100, 100, 0.4);
                position: absolute;
            }
            
            .ace_warning {
                background-color: rgba(255, 165, 0, 0.2);
                position: absolute;
                z-index: 5;
            }
            
            .ace_lint-tooltip {
                background-color: #ffffff;
                border: 1px solid #dee2e6;
                color: #212529;
                padding: 5px 10px;
                border-radius: 4px;
                font-size: 12px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
            }
        </style>
        """, unsafe_allow_html=True)

# -------- Splash Screen --------
def show_splash_screen():
    # Create a centered column layout with more emphasis on the center
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Create a container to center content
        with st.container():
            # Center the logo with CSS
            st.markdown(
                """
                <div style='display: flex; justify-content: center;'>
                    <img src='https://raw.githubusercontent.com/sivaramaraju2124/CodeForge/main/logo.jpeg
' width='200'>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Add title and subtitle centered
            st.markdown("<h2 style='text-align: center; margin-top: 10px;'>CodeForge</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; margin-bottom: 20px;'>AI-Powered Code Editor</p>", unsafe_allow_html=True)
        
        # Add animated progress bar
        progress_text = "Initializing application..."
        st.text(progress_text)
        my_bar = st.progress(0)
        
        for percent_complete in range(100):
            time.sleep(0.02)  # Adjust speed of loading here
            my_bar.progress(percent_complete + 1)
        
        # Once progress reaches 100%, clear the splash screen
        st.session_state.loading_complete = True
        st.rerun()

# Helper function to load image from file and convert to base64
def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')
# -------- App Configuration --------
st.set_page_config(
    page_title="CodeForge | AI-Powered IDE",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize loading state in session state
if "loading_complete" not in st.session_state:
    st.session_state.loading_complete = False

# Show splash screen if loading is not complete
if not st.session_state.loading_complete:
    show_splash_screen()
    st.stop()  # Stop the rest of the app from loading

# Initialize theme preference in session state
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# Load the appropriate CSS based on current theme
load_css(st.session_state.theme)

# Initialize theme toggle function
def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
    # No need to explicitly reload CSS here, it will be loaded on rerun

# -------- Header & Navigation --------
col1, col2 = st.columns([10, 2])
with col1:
    st.markdown("# 💻 CodeForge")
    st.markdown("<p style='margin-bottom: 20px;'>Advanced AI-Powered Code Editor with Groq</p>", unsafe_allow_html=True)

with col2:
    # Theme toggle button with appropriate icon based on current theme
    theme_icon = "🌙" if st.session_state.theme == "light" else "☀"
    theme_label = "Dark Mode" if st.session_state.theme == "light" else "Light Mode"
    
    if st.button(f"{theme_icon} {theme_label}", key="theme_toggle"):
        toggle_theme()
        st.rerun()

# Navigation Bar
selected_nav = option_menu(
    menu_title=None,
    options=["Editor", "Image to Code", "Generator", "Settings"],
    icons=["code-slash", "camera", "lightning", "gear"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#282a36" if st.session_state.theme == "dark" else "#f8f9fa", "margin-bottom": "20px"},
        "icon": {"color": "#bd93f9" if st.session_state.theme == "dark" else "#3949ab", "font-size": "14px"},
        "nav-link": {"font-size": "14px", "text-align": "center", "margin": "0px", "--hover-color": "#44475a" if st.session_state.theme == "dark" else "#e9ecef"},
        "nav-link-selected": {"background-color": "#6272a4" if st.session_state.theme == "dark" else "#3949ab"},
    }
)

# -------- Sidebar --------
with st.sidebar:
    st.markdown("### ⚙ Editor Settings")
    
    language = st.selectbox(
        "Programming Language",
        list(judge0_language_ids.keys()),
        index=0,
        help="Select your preferred programming language"
    )
    
    with st.expander("🎨 Theme Settings", expanded=True):
        theme = st.selectbox(
            "Editor Theme",
            ["monokai", "github", "dracula", "solarized_dark", "solarized_light", "terminal"],
            index=0,
            help="Choose theme for your editor."
        )
        font_size = st.slider("Font Size", 12, 24, 16,help="Select your font size")
        show_gutter = st.checkbox("Show Line Numbers", value=True)
        wrap_text = st.checkbox("Wrap Text", value=False)
    
    with st.expander("⌨ Keyboard Shortcuts"):
        st.markdown("""
        - Save: Ctrl+S
        - Find: Ctrl+F
        - Replace: Ctrl+H
        - Comment: Ctrl+/
        """)
    
    st.markdown("---")
    st.markdown("<div style='text-align: center;'>💻 CodeForge<br><small>v1.0.0</small></div>", unsafe_allow_html=True)

# Default code templates
default_code = {
    "python": 'print("Hello, World!")',
    "javascript": 'console.log("Hello, World!");',
    "java": '''public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}''',
    "c_cpp": '''#include <stdio.h>
int main() {
    printf("Hello, World!\\n");
    return 0;
}''',
    "bash": 'echo "Hello, World!"'
}

# Initialize session state for code
if f"editor-{language}" not in st.session_state:
    st.session_state[f"editor-{language}"] = default_code[language]

if "console_output" not in st.session_state:
    st.session_state.console_output = ""

# -------- Image to Code Function --------
def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def extract_code_with_groq(image, language):
    base64_image = encode_image(image)
    prompt = f"Please extract the code from this image and convert it into {language}. Output only the code with main method and without any explanations or markdown."

    try:
        with st.spinner("🪄 AI is analyzing your image..."):
            response = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ],
                }]
            )

            result = response.choices[0].message.content.strip()

            if result.startswith("") and result.endswith(""):
                result = result.strip("`").strip()
                lines = result.split("\n")
                if lines[0].strip().lower() == language.lower():
                    result = "\n".join(lines[1:])
                else:
                    result = "\n".join(lines)

            return result.strip()

    except Exception as e:
        st.error(f"⚠ Error extracting code: {e}")
        return ""

# -------- Code Generation Function --------
def generate_with_groq(prompt, language):
    try:
        with st.spinner("🤖 AI is generating your code..."):
            full_prompt = f"Write complete code in {language} for: {prompt}. Only code, no explanation."
            headers = {
                "Authorization": f"Bearer {openai.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "llama3-8b-8192",
                "messages": [{"role": "user", "content": full_prompt}]
            }

            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=data
            )

            result = response.json()
            content = result["choices"][0]["message"]["content"].strip()

            if content.startswith("") and content.endswith(""):
                content = content.strip("`").strip()
                lines = content.split("\n")
                if lines[0].strip().lower() == language.lower():
                    content = "\n".join(lines[1:])
                else:
                    content = "\n".join(lines) 

            return content.strip()

    except Exception as e:
        st.error(f"⚠ Groq Error: {e}")
        return ""
# -------- share Code Function --------
PASTEBIN_API_KEY = "EOXKfS2zH6KArbHi1Huiu9_iRCFGD7_T"  # replace with your actual API key

def create_pastebin_link(code, title="CodeForge Snippet", language="python"):
    try:
        data = {
            'api_dev_key': PASTEBIN_API_KEY,
            'api_option': 'paste',
            'api_paste_code': code,
            'api_paste_name': title,
            'api_paste_format': language,
            'api_paste_private': 1,  # 0=public, 1=unlisted, 2=private
            'api_paste_expire_date': '1W'
        }

        response = requests.post("https://pastebin.com/api/api_post.php", data=data)

        if response.status_code == 200 and "http" in response.text:
            return response.text.strip()
        else:
            return f"Error uploading to Pastebin: {response.text}"
    except Exception as e:
        return f"Exception: {e}"

# -------- Run Code Function --------
def run_code(code, language, user_input):
    try:
        with st.spinner("⚙ Compiling and running your code..."):
            lang_id = judge0_language_ids[language]
            payload = {
                "language_id": lang_id,
                "source_code": code,
                "stdin": user_input,
                "base64_encoded": False
            }

            query = {"base64_encoded": "false", "fields": "*"}
            res = requests.post(JUDGE0_URL, headers=JUDGE0_HEADERS, json=payload, params=query)

            if res.status_code == 201:
                token = res.json().get("token")
                if token:
                    # Progress bar for execution
                    progress_bar = st.progress(0)
                    for i in range(5):
                        time.sleep(0.6)
                        progress_bar.progress((i + 1) * 20)
                        
                    result = requests.get(f"{JUDGE0_URL}/{token}", headers=JUDGE0_HEADERS, params=query).json()
                    output = result.get("stdout") or ""
                    error = result.get("stderr") or result.get("compile_output") or ""
                    
                    if error:
                        return error, "error"
                    elif output:
                        return output, "success"
                    else:
                        return "Program executed with no output", "info"
                else:
                    return "Error: Judge0 did not return a token.", "error"
            else:
                return f"Judge0 API Error: {res.status_code} - {res.text}", "error"

    except Exception as e:
        return f"Execution Error: {e}", "error"

# Initialize session state for code
if f"editor-{language}" not in st.session_state:
    st.session_state[f"editor-{language}"] = default_code[language]

if "console_output" not in st.session_state:
    st.session_state.console_output = ""

# Handle navigation between pages
if "navigate_to" in st.session_state:
    selected_nav = st.session_state.navigate_to
    del st.session_state.navigate_to  # Clear the flag after navigating

# -------- Content Based on Navigation --------
if selected_nav == "Editor":
    # Main code editor tab
    col1, col2 = st.columns([10, 3])
    
    with col1:
        st.markdown("### ✏ Code Editor")
        
        # Code editor
        code = st_ace(
            value=st.session_state[f"editor-{language}"],
            language=language,
            theme=theme,
            font_size=font_size,
            show_gutter=show_gutter,
            wrap=wrap_text,
            auto_update=True,
            key=f"ace-editor-{language}"
        )
        
        # Save code to session state
        if code != st.session_state[f"editor-{language}"]:
            st.session_state[f"editor-{language}"] = code
        
        # Tool buttons
        col_run, col_download, col_share = st.columns([1, 1, 1])  # Added column for copy button
        
        with col_run:
            run_button = st.button("▶ Run Code", use_container_width=True,help="Run your code")
        
        with col_download:
            st.download_button(
                label="📥 Download",
                data=code,
                file_name=f"codeforge_{language.lower()}.{'py' if language == 'python' else language.lower()}",
                mime="text/plain",
                use_container_width=True,
                help="Download your code as a file"
            )
        
        with col_share:
            share_button = st.button("🔗 Share Code", use_container_width=True,help="Share your code to others")
            if share_button:
                link = create_pastebin_link(code, language=language.lower())
                st.markdown(f"### Copy this link to share with others:")
                st.code(link, language='text')

    with col2:
        # Input for program
        st.markdown("### 🖥 Console")
        user_input = st.text_area("Input (stdin)", "", height=100)
        
        # Run code and show output
        if run_button:
            output, status = run_code(code, language, user_input)
            st.session_state.console_output = output
            
            if status == "error":
                # Using custom HTML for error message styling
                st.markdown(f"""
                <div style='padding:10px; background-color:#ffdddd; color:#a94442; border:1px solid #ebccd1; border-radius:4px;'>
                    ❌ {output}
                </div>
                """, unsafe_allow_html=True)

            elif status == "info":
                st.markdown(f"""
                <div style='padding:10px; background-color:#d9edf7; color:#31708f; border:1px solid #bce8f1; border-radius:4px;'>
                    ℹ {output}
                </div>
                """, unsafe_allow_html=True)

            else:
                success_message = "Code executed successfully!"
                st.markdown(f"""
                <div style='padding:10px; background-color:#dff0d8; color:#3c763d; border:1px solid #d6e9c6; border-radius:4px;'>
                    ✅ {success_message}
                </div>
                """, unsafe_allow_html=True)
                
        # Console output
        st.text_area("Output", st.session_state.console_output, height=300)

        
#         st.markdown("""
# <div style="background-color:#fffae6; padding:10px; border-left: 5px solid #f9a825; border-radius:5px; font-weight:bold;">
# ⌨ Press CTRL + Enter in the editor to update the code before running!
# </div>
# """, unsafe_allow_html=True)


elif selected_nav == "Image to Code":
    st.markdown("### 📷 Image to Code Converter")
    st.markdown("Upload an image of handwritten code or a screenshot and our AI will convert it to executable code.")
    
    # Image upload section
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Display image and extracted code
        col1, col2 = st.columns([1, 1])
        
        with col1:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
        
        with col2:
            extract_button = st.button("🪄 Extract Code", use_container_width=True)
            
            if extract_button:
                extracted_code = extract_code_with_groq(image, language)
                
                if extracted_code:
                    st.session_state[f"editor-{language}"] = extracted_code
                    st.success("✅ Code extracted successfully!")
                    st.code(extracted_code, language=language.lower())
                    
                    if st.button("📋 Use This Code in Editor", use_container_width=True, key="img_to_editor"):
                        st.session_state[f"editor-{language}"] = extracted_code
                        st.session_state.navigate_to = "Editor"  # Set a flag for navigation
                        st.rerun()  # Rerun to update the state
                else:
                    st.error("❌ Failed to extract code from image.")
    
    # Tips for better results
    with st.expander("💡 Tips for Better Results"):
        st.markdown("""
        - Ensure good lighting and a clear image
        - Make handwriting as legible as possible
        - Avoid shadows across the page
        - Keep lines of code separated and clear
        - Check the extracted code carefully before running
        """)

elif selected_nav == "Generator":
    st.markdown("### 🤖 AI Code Generator")
    st.markdown("Let our AI generate code for you based on your description.")
    
    # Code generation
    prompt = st.text_area("Describe the code you want to generate", 
                          placeholder="Example: Write a function to find the Fibonacci sequence up to n terms")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        generate_button = st.button("✨ Generate Code", use_container_width=True)
    
    if generate_button and prompt:
        generated_code = generate_with_groq(prompt, language)
        
        if generated_code:
            st.session_state[f"editor-{language}"] = generated_code
            
            st.success("✅ Code generated successfully!")
            st.code(generated_code, language=language.lower())
            
            if st.button("📋 Use This Code in Editor", use_container_width=True, key="gen_to_editor"):
                st.session_state[f"editor-{language}"] = generated_code
                st.session_state.navigate_to = "Editor"  # Set a flag for navigation
                st.rerun()  # Rerun to update the state
    
    # Example prompts
    with st.expander("💡 Example Prompts"):
        example_prompts = {
            "python": [
                "Create a function to check if a string is a palindrome",
                "Write a program to scrape a website and save data to CSV",
                "Create a simple Flask API with two endpoints"
            ],
            "javascript": [
                "Create a function to filter an array of objects by property value",
                "Write a simple React component for a todo list",
                "Create a function to calculate the average of an array of numbers"
            ],
            "java": [
                "Create a class to represent a bank account with deposit and withdraw methods",
                "Write a program to read a CSV file and process its contents",
                "Create a simple REST API using Spring Boot"
            ],
            "c_cpp": [
                "Write a function to find the greatest common divisor of two numbers",
                "Create a linked list implementation with insert and delete methods",
                "Write a program to sort an array using quicksort"
            ],
            "bash": [
                "Create a script to backup files modified in the last 24 hours",
                "Write a script to monitor system resources and send alerts",
                "Create a script to find and delete duplicate files in a directory"
            ]
        }
        
        st.markdown(f"Example prompts for {language}:")
        for example in example_prompts[language]:
            if st.button(example, key=f"example_{example[:20]}"):
                st.session_state.prompt = example
                st.rerun()
elif selected_nav == "Settings":
    st.markdown("### ⚙ Settings")
    
    # Interface settings
    with st.expander("🎛 Interface Settings"):
        st.checkbox("Dark Mode (System Default)", value=True, key="dark_mode_checkbox")
        st.checkbox("Show Line Numbers", value=True, key="line_numbers_checkbox")
        st.checkbox("Auto-save Code", value=True, key="auto_save_checkbox")
        st.select_slider("Code Editor Width", options=["Small", "Medium", "Large", "Full Width"], value="Large", key="editor_width_slider")

    
    # About section
    with st.expander("ℹ About CodeForge"):
        st.markdown("""
        CodeForge is an advanced AI-powered online code editor that combines:
        
        - Real-time code editing and execution using Judge0
        - AI code generation powered by Groq's LLama models
        - Image-to-code conversion for handwritten code
        
        Built with Streamlit and enhanced with custom styling to provide a professional development environment.
        
        Version: 1.0.0  
        Last Updated: April 2025
        """)
# -------- ChatBot --------
LABELS = {
    "en": {"user": "You", "bot": "CodeBot"},
    # Add more languages if needed
}

LANGUAGES = {
    "English": "en",
    # Add more languages if needed
}

conn = sqlite3.connect("chat_history.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        language TEXT,
        sender TEXT,
        message TEXT
    )
""")
conn.commit()

# Define the function to get the response from the Groq API
def get_groq_response(user_input, language_code):
    prompt = f"""
You are an expert AI assistant that generates code and explains it in simple terms.
The user is asking for help with coding.
Speak in the selected language ({language_code}).
User's Question: {user_input}
Answer:"""
    response = client.chat.completions.create(
        model="llama3-8b-8192",  # Replace with the appropriate Groq model
        messages=[{"role": "user", "content": user_input}],
    )
    return response.choices[0].message.content.strip()

# Initialize the chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "assistant", "content": "I am CodeBot, ready to help you with your coding questions!"}]
# Chat toggle button
if "show_bot" not in st.session_state:
    st.session_state.show_bot = False

# Create a centered column for the chat toggle button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("💬 Chat with CodeBot", use_container_width=True):
        st.session_state.show_bot = not st.session_state.show_bot  # Toggle chat visibility

if st.session_state.show_bot:
    # Add a wrapper for centering the chat
    st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)
    
    # Chat container with limited width
    st.markdown("""
    <div class="chat-container">
        <div class="chat-header">
            <h3>💬 CodeBot</h3>
        </div>
    """, unsafe_allow_html=True)


    # Default action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        explain_clicked = st.button("🧠 Explain Code")
    with col2:
        error_clicked = st.button("🐞 Find Errors")
    with col3:
        optimize_clicked = st.button("⚙ Optimize Code")

    # Handle action button logic
    instruction = None
    if explain_clicked and code.strip():
        instruction = "Explain the following code in simple terms:\n\n" + code
    elif error_clicked and code.strip():
        instruction = "Find and fix errors in the following code:\n\n" + code
    elif optimize_clicked and code.strip():
        instruction = "Optimize the following code for better performance and readability:\n\n" + code

    if instruction:
        st.session_state.chat_history.append({"role": "user", "content": instruction})
        try:
            with st.spinner("CodeBot is working..."):
                response = get_groq_response(instruction, "en")
                reply = response
        except Exception as e:
            reply = f"An error occurred: {e}"
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

    # Display messages
    for msg in st.session_state.chat_history:
        role = "You" if msg["role"] == "user" else "CodeBot"
        msg_class = "user-msg" if msg["role"] == "user" else "bot-msg"
        
        st.markdown(f"""
            <div class="message-container">
                <div class="{msg_class}">
                    <div class="sender-name">{role}</div>
                    {msg["content"]}
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Create container for input
    st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
    
    # Input for user message
    user_input = st.text_input("", placeholder="Type your message here...", key="user_input_key", 
                              value=st.session_state.get('user_input', ''))
    
    # Send button
    if st.button("Send", key="chat_send_button", use_container_width=True):
        if user_input.strip() != "":
            # Process message and update chat
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            try:
                with st.spinner("CodeBot is thinking..."):
                    response = get_groq_response(user_input, "en")
                    reply = response
            except Exception as e:
                reply = f"An error occurred: {e}"
            
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.session_state.user_input = ""
            st.rerun()

    # Close the input container
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Close the chat container
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Close the wrapper
    st.markdown('</div>', unsafe_allow_html=True)

# Update the CSS styling for the chat container to limit width and improve alignment
st.markdown("""
    <style>
        /* Chat container styling - limiting width */
        .chat-container {
            background-color: #282a36;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            margin: 20px auto;
            border: 1px solid #44475a;
            max-width: 600px; /* Limit the width */
            width: 90%; /* Responsive width */
        }
        
        /* Message container */
        .message-container {
            display: flex;
            margin-bottom: 12px;
            flex-direction: column;
        }
        
        /* User message styling */
        .user-msg {
            background-color: #6272a4;
            color: white;
            border-radius: 12px 12px 0 12px;
            padding: 10px 15px;
            margin: 5px 0;
            max-width: 80%;
            align-self: flex-end;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-left: auto;
            word-wrap: break-word;
        }
        
        /* Bot message styling */
        .bot-msg {
            background-color: #44475a;
            color: #f8f8f2;
            border-radius: 12px 12px 12px 0;
            padding: 10px 15px;
            margin: 5px 0;
            max-width: 80%;
            align-self: flex-start;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-right: auto;
            word-wrap: break-word;
        }
        
        /* Sender name styling */
        .sender-name {
            font-weight: 600;
            margin-bottom: 3px;
            font-size: 0.9em;
            opacity: 0.8;
        }
        
        /* Chat header styling */
        .chat-header {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid #44475a;
        }
        
        .chat-header h3 {
            margin: 0;
            color: #bd93f9;
        }
        
        /* Chat input container */
        .chat-input-container {
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-top: 15px;
        }
        
        /* Streamlit specific overrides for chatbot */
        .stButton > button.chat-send-btn {
            background-color: #6272a4 !important;
            color: white !important;
            border-radius: 20px !important;
            padding: 0.3rem 1.5rem !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            border: none !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button.chat-send-btn:hover {
            background-color: #bd93f9 !important;
            transform: translateY(-2px) !important;
        }
        
        /* Ensure the chat appears in center of its container */
        .chat-wrapper {
            display: flex;
            justify-content: center;
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)


# Footer
st.markdown("---")
st.markdown(
    """
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0;">
        <div>
            <small>Powered by Groq AI + Judge0 + Streamlit</small>
        </div>
        <div>
            <small>© 2025 CodeForge • All Rights Reserved</small>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
    
# Contact Us section
with st.expander("📬 Contact Us"):
    st.markdown("""
    Have feedback or need help? Reach out to us!
    
    - 📧 Email: [support@codeforge.ai](mailto:swamisivaramaraju@gmail.com)    
    - 🌐 Website: [www.codeforge.ai](https://code-forge.streamlit.app/)  
    """)
