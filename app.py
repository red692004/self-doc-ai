import streamlit as st
from google import genai

# Page Configuration & Search Engine Optimization (SEO) Metadata
st.set_page_config(
    page_title="Self Doc AI - Trusted Health & Medicine Guide Bangladesh",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional medical styling & interactive buttons
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
    .stButton button {
        background-color: #1e293b;
        color: #38bdf8;
        border: 1px solid #38bdf8;
        border-radius: 8px;
        width: 100%;
    }
    .stButton button:hover {
        background-color: #38bdf8;
        color: #0f172a;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Configuration & Language Selection
st.sidebar.header("⚙️ Settings & Options")
language_choice = st.sidebar.selectbox(
    "Choose Language / ভাষা নির্বাচন করুন:",
    ["English", "Bangla (বাংলা)"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ About Self Doc AI")
st.sidebar.info(
    "Designed for Bangladesh. Provides preliminary educational health information and connects users with medical guidance."
)

# Main Title & Subtitle based on language selection
if language_choice == "Bangla (বাংলা)":
    st.title("🩺 সেলফ ডক এআই (Self Doc AI)")
    st.markdown("### বাংলাদেশের জন্য আপনার বিশ্বস্ত স্বাস্থ্য ও ওষুধের তথ্য সহায়িকা")
    subtitle_text = "ওষুধের ব্যবহার, সাধারণ মাত্রা এবং স্বাস্থ্য সচেতনতা সম্পর্কিত নির্ভরযোগ্য তথ্য জেনে নিন।"
    search_label = "🔍 আপনার স্বাস্থ্য বা ওষুধ সংক্রান্ত প্রশ্ন এখানে লিখুন (বাংলা বা ইংরেজিতে):"
    guidance_title = "📋 শিক্ষণীয় পরামর্শ"
    safety_text = "⚠️ **সতর্কতা:** যেকোনো ওষুধ সেবন করার পূর্বে অবশ্যই বাংলাদেশের একজন রেজিস্টার্ড এমবিবিএস ডাক্তার বা ফার্মাসিস্টের পরামর্শ নিন।"
else:
    st.title("🩺 Self Doc AI")
    st.markdown("### Your Safe, Trusted Educational Health Companion for Bangladesh")
    subtitle_text = "Get instant, reliable educational information about common medicines, standard usages, and safety guidelines."
    search_label = "🔍 Or type your health or medicine question below (English, Bangla, or Banglish):"
    guidance_title = "📋 Educational Guidance"
    safety_text = "⚠️ **Safety Notice:** Always consult a registered MBBS doctor or pharmacist in Bangladesh before taking any medication."

# Fetch API key securely from Streamlit server secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("⚠️ API Key is not configured on the server. Please add it to Streamlit Secrets.")
    api_key = None

# Main navigation tabs
tab1, tab2, tab3 = st.tabs(["🤖 AI Health Guide", "💬 Free Doctor Consultation", "⭐ Paid Expert Consultation"])

with tab1:
    st.write(subtitle_text)
    
    # Quick-Click Preset Query Buttons for Common Topics
    st.markdown("#### 💡 Quick Health Topics (Click to Check):")
    col1, col2, col3 = st.columns(3)

    selected_query = ""
    with col1:
        if st.button("Paracetamol Info"):
            selected_query = "What are the standard educational guidelines and age-based precautions for taking Paracetamol in Bangladesh?"
    with col2:
        if st.button("Cold & Fever Care"):
            selected_query = "What are safe home remedies and general educational guidelines for common cold and fever?"
    with col3:
        if st.button("Antacid Guidance"):
            selected_query = "What is the general educational guidance on taking antacids for acidity?"

    # Text input for custom searches
    user_query = st.text_input(search_label, value=selected_query)

    if user_query and api_key:
        with st.spinner("Analyzing safely..." if language_choice == "English" else "বিশ্লেষণ করা হচ্ছে..."):
            try:
                client = genai.Client(api_key=api_key)
                
                # Instruction to force the AI to match the chosen language
                lang_instruction = "Reply entirely in fluent Bangla." if language_choice == "Bangla (বাংলা)" else "Reply in clear English."
                
                prompt = f"""
                You are an AI medical educational assistant for Bangladesh. 
                The user is asking about: {user_query}
                {lang_instruction}
                Provide clear, structured educational information about common medicine usage, standard classifications, and safety precautions.
                Always remind the user to consult a registered MBBS doctor or pharmacist in Bangladesh.
                """
                response = client.models.generate_content(model="gemini-3.8-flash", contents=prompt)
                
                st.markdown("---")
                st.markdown(f"### {guidance_title}")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")

        st.warning(safety_text)

with tab2:
    st.markdown("### 💬 Free Doctor Consultation (Community Queue)")
    st.markdown("""
    *Connect with on-duty volunteer medical students and general practitioners for basic case reviews.*
    
    * **Status:** 🚧 **Coming Soon** — We are currently onboarding verified doctors and medical volunteers in Bangladesh.
    * **How it will work:** Submit your case history and reports here to enter the community consultation queue for a free preliminary evaluation.
    """)
    st.info("Stay tuned! This feature will go live as soon as our initial doctor network partnerships are finalized.")

with tab3:
    st.markdown("### ⭐ Paid Expert Consultation (Specialist Booking)")
    st.markdown("""
    *Book direct video appointments or priority text chats with verified specialist physicians (Cardiologists, Pediatricians, Gynecologists, etc.).*
    
    * **Status:** 🚧 **Coming Soon** — Integrated bKash/Nagad payment gateways and secure video scheduling are under development.
    * **Benefits:** Guaranteed rapid response times, prescription generation by certified specialists, and direct follow-up chats.
    """)
    st.success("Doctor applications and partnership onboarding will open during Phase 2 of our launch roadmap!")
