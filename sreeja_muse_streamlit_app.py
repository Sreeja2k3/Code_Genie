import streamlit as st
import pytesseract
from PIL import Image
import pdfplumber
import io
import datetime

# If Tesseract installed manually, uncomment & update path
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

st.set_page_config(page_title="Smart AI Assistant", layout="wide")

# -------------------------------
# Custom CSS (Premium UI)
# -------------------------------
st.markdown("""
    <style>
    body { background-color: #111; }
    .main { background-color: #111; }
    .stTextInput>div>div>input {
        background-color: #222;
        color: white;
        border-radius: 8px;
    }
    .stTextArea textarea {
        background-color: #222;
        color: white;
        border-radius: 8px;
    }
    .chat-bubble-user {
        background-color: #007BFF;
        color: white;
        padding: 10px;
        border-radius: 10px;
        width: fit-content;
        margin-bottom: 5px;
    }
    .chat-bubble-bot {
        background-color: #FFD966;
        color: black;
        padding: 10px;
        border-radius: 10px;
        width: fit-content;
        margin-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# Chat History Storage
# -------------------------------
if "chat" not in st.session_state:
    st.session_state.chat = []

# -------------------------------
# Sidebar Menu
# -------------------------------
st.sidebar.title("📌 Menu")

page = st.sidebar.radio(
    "Select Mode:",
    ["🤖 Smart Chatbot", "🧑‍💻 Code Assistant", "📄 OCR Extractor"]
)

st.sidebar.markdown("---")
if st.sidebar.button("Clear Chat"):
    st.session_state.chat = []
    st.rerun()

# -------------------------------
# Chat Display Function
# -------------------------------
def display_chat():
    for role, msg in st.session_state.chat:
        if role == "user":
            st.markdown(f"<div class='chat-bubble-user'>{msg}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-bubble-bot'>{msg}</div>", unsafe_allow_html=True)

# -------------------------------
# Dummy AI Response Generator
# -------------------------------
def ai_reply(text):
    return f"Here's a helpful, friendly explanation based on what you asked:\n\n{text}"

# ------------------------------------------------
# 1️⃣ SMART CHATBOT PAGE
# ------------------------------------------------
if page == "🤖 Smart Chatbot":
    st.title("🤖 Smart Chatbot Interface")

    display_chat()

    user_input = st.text_input("Type your question here...")

    if st.button("Send"):
        if user_input.strip():
            st.session_state.chat.append(("user", user_input))
            bot_res = ai_reply(user_input)
            st.session_state.chat.append(("bot", bot_res))
            st.rerun()

# ------------------------------------------------
# 2️⃣ CODE ASSISTANT PAGE (UPDATED)
# ------------------------------------------------
elif page == "🧑‍💻 Code Assistant":
    st.title("🧑‍💻 AI Code Assistant")

    code_query = st.text_area("Describe your coding problem:")

    if st.button("Get Code Help"):
        if code_query.strip():

            # Simple rule-based generator
            def generate_code(question):

                q = question.lower()

                if "multiply" in q and "two numbers" in q:
                    return """# Python code to multiply two numbers
a = int(input("Enter first number: "))
b = int(input("Enter second number: "))

result = a * b
print("Multiplication:", result)
"""

                elif "add" in q and "two numbers" in q:
                    return """# Python code to add two numbers
a = int(input("Enter first number: "))
b = int(input("Enter second number: "))

print("Sum =", a + b)
"""

                elif "factorial" in q:
                    return """# Python program to find factorial
num = int(input("Enter a number: "))

fact = 1
for i in range(1, num + 1):
    fact *= i

print("Factorial =", fact)
"""

                elif "largest" in q:
                    return """# Python program to find largest of three numbers
a = int(input("Enter first number: "))
b = int(input("Enter second number: "))
c = int(input("Enter third number: "))

print("Largest =", max(a, b, c))
"""

                else:
                    return "# Sorry, no matching code found. Add more rules in generate_code()."

            st.write("### 🔍 Suggested Solution")
            st.code(generate_code(code_query), language="python")

# ------------------------------------------------
# 3️⃣ OCR EXTRACTOR PAGE
# ------------------------------------------------
elif page == "📄 OCR Extractor":
    st.title("📄 OCR Text Extractor")

    uploaded_file = st.file_uploader("Upload an image or PDF", type=["png", "jpg", "jpeg", "pdf"])

    if uploaded_file:

        # If PDF
        if uploaded_file.type == "application/pdf":
            with pdfplumber.open(uploaded_file) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
            st.text_area("Extracted Text:", text, height=300)

        # If Image
        else:
            img = Image.open(uploaded_file)
            text = pytesseract.image_to_string(img)
            st.text_area("Extracted Text:", text, height=300)


