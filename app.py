import streamlit as st
import os
from google import genai

# Page Configuration
st.set_page_config(
    page_title="Self Doc AI",
    page_icon="🩺",
    layout="centered"
)

# Custom CSS for a clean, professional medical aesthetic & background styling
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
        font-family: "Helvetica Neue", sans-serif;
    }
    .stTextInput input {
        background-color: #1e293b;
        color: #ffffff;
        border: 1px solid #38bdf8;
        border-radius: 8px;
    }
    .stAlert {
        background-color: #1e293b !important;
        color: #f8fafc !important;
        border: 1px solid #cbd5e1;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🩺 Self Doc AI")
st.markdown("### Your Safe, Trusted Educational Health Companion for Bangladesh")
st.write("Find clear educational information about common medicines, standard usages, and safety guidelines instantly.")

# Sidebar for API Key
st.sidebar.header("⚙️ Configuration")
api_key_input = st.sidebar.text_input("Enter your Google Gemini API Key:", type="password")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🌟 Coming Soon")
st.sidebar.markdown("- Verified Doctor Consultations")
st.sidebar.markdown("- Symptom Specialist Matching")

user_query = st.text_input("🔍 What medicine or symptom would you like to check? (Type in English, Bangla, or Banglish):")

if user_query:
    if not api_key_input:
        st.error("⚠️ Please enter your Google Gemini API Key in the sidebar on the left first!")
    else:
        with st.spinner("Self Doc AI is analyzing safely..."):
            try:
                client = genai.Client(api_key=api_key_input)
                
                prompt = f"""
                You are an AI medical educational assistant for Bangladesh. 
                The user is asking in English, Bangla, or Banglish about: {user_query}
                Provide general educational information about common medicine usage, standard age-based classifications, and safety precautions.
                If the user writes in Bangla or Banglish, reply clearly in an easy-to-understand manner.
                Always remind the user to consult a registered MBBS doctor or pharmacist in Bangladesh.
                """
                
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt,
                )
                
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}. Please check that your API key is correct.")

    st.warning("⚠️ **Safety Notice:** Always consult a registered MBBS doctor or pharmacist in Bangladesh before taking any medication.")
