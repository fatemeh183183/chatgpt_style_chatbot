
import streamlit as st
from PIL import Image
import pytesseract
import os
from dotenv import load_dotenv
from openai import OpenAI
import io

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

# Session state for memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Streamlit app layout
st.set_page_config(page_title="ChatGPT-style Bot (Text + Image)", layout="wide")
st.title("🧠 ChatGPT-style Multimodal Chatbot")
st.write("Chat with text and image inputs. Ask about uploaded photos, charts, documents, and more!")

# Sidebar for image upload
with st.sidebar:
    st.header("📷 Upload an Image")
    uploaded_image = st.file_uploader("Upload .jpg, .png", type=["jpg", "jpeg", "png"])
    image_text = ""

    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Use pytesseract as backup OCR
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='PNG')
        image_bytes = image_bytes.getvalue()

        try:
            response = client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that understands images."},
                    {"role": "user", "content": [
                        {"type": "text", "text": "What’s in this image?"},
                        {"type": "image_url", "image_url": {
                            "url": "data:image/png;base64," + image_bytes.encode('base64').decode()
                        }}
                    ]}
                ],
                max_tokens=500
            )
            image_text = response.choices[0].message.content
        except:
            st.warning("GPT-4 Vision not available. Using OCR fallback.")
            image_text = pytesseract.image_to_string(image)

        st.session_state.messages.append({"role": "user", "content": "Here's an image I uploaded."})
        st.session_state.messages.append({"role": "assistant", "content": image_text})

# Chat area
st.subheader("💬 Start Chatting")

user_input = st.text_input("You:", key="user_input")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages],
            max_tokens=1000
        )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"🧑‍💻 **You**: {msg['content']}")
    else:
        st.markdown(f"🤖 **Bot**: {msg['content']}")
