🤖 ChatGPT-Style Multimodal Chatbot (Text + Image)
This is a ChatGPT-like chatbot built with Streamlit. You can:

Ask any question using text
Upload an image and ask questions about its content
Use GPT-4 Vision (if your OpenAI key supports it) or fallback to OCR
Continue your chat with context memory
📦 Features
🖼 Image understanding via GPT-4 Vision or OCR
🧠 Memory: Chat history persists during session
🎯 ChatGPT-style interface (text + visual)
✅ Easy Streamlit UI, ready for deployment
🚀 How to Use
Install the required packages:
pip install -r requirements.txt
Add your OpenAI API key to .env:
OPENAI_API_KEY=your_openai_key_here
Run the app:
streamlit run chatgpt_style_chatbot.py
🔒 Requirements
OpenAI GPT-4 access (optional: GPT-4 Vision)
Python 3.8+
🧠 Tech Stack
Streamlit
OpenAI API (GPT-4 + GPT-4-Vision)
pytesseract (backup OCR)
PIL (for image handling)
