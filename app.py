import streamlit as st
from google import genai

st.set_page_config(page_title="Self Doc AI", page_icon="🩺", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(15, 23, 42, 0.85), rgba(15, 23, 42, 0.85)), 
                    url("https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=1920&q=80");
        background-size: cover;
        background-position: center;
        color: #ffffff;
    }
    h1, h2, h3 {
        color: #38bdf8 !important;
    }
    .stTextInput input {
        background-color: #1e293b;
        color: #ffffff;
        border: 1px solid #38bdf8;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🩺 Self Doc AI")
st.markdown("### Your Safe, Trusted Educational Health Companion for Bangladesh")

# Fetch API key securely from Streamlit server secrets (no user input needed!)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("⚠️ API Key is not configured on the server. Please add it to Streamlit Secrets.")
    api_key = None

user_query = st.text_input("🔍 What medicine or symptom would you like to check? (Type in English, Bangla, or Banglish):")

if user_query and api_key:
    with st.spinner("Self Doc AI is analyzing safely..."):
        try:
            client = genai.Client(api_key=api_key)
            prompt = f"""
            You are an AI medical educational assistant for Bangladesh. 
            The user is asking in English, Bangla, or Banglish about: {user_query}
            Provide general educational information about common medicine usage and safety precautions.
            Always remind the user to consult a registered MBBS doctor or pharmacist in Bangladesh.
            """
            response = client.models.generate_content(model="gemini-3.8-flash", contents=prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"An error occurred: {e}")

    st.warning("⚠️ **Safety Notice:** Always consult a registered MBBS doctor or pharmacist in Bangladesh before taking any medication.")
