import streamlit as st
from google import genai

# Page Configuration & SEO
st.set_page_config(
    page_title="Self Doc AI - Trusted Health & Medicine Guide Bangladesh",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject Google Search Console Verification Meta Tag into the Web Header
st.markdown(
    '<meta name="google-site-verification" content="google36f49e9d23fb7ae3" />',
    unsafe_allow_html=True
)

# Custom High-End Modern Medical Styling CSS
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.90)), 
                    url("https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=1920&q=80");
        background-size: cover;
        background-position: center;
        color: #f8fafc;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    h1, h2, h3 {
        color: #38bdf8 !important;
        font-weight: 700;
    }

    .stTextInput input {
        background-color: rgba(30, 41, 59, 0.8) !important;
        color: #ffffff !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 12px !important;
        padding: 14px !important;
        font-size: 16px !important;
    }
    .stTextInput input:focus {
        border-color: #7dd3fc !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.3);
    }

    .stButton button {
        background-color: rgba(30, 41, 59, 0.9);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.4);
        border-radius: 10px;
        padding: 10px 16px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton button:hover {
        background-color: #38bdf8;
        color: #0f172a;
        border-color: #38bdf8;
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# Top Header Layout
header_col1, header_col2 = st.columns([3, 1])

with header_col1:
    st.title("🩺 Self Doc AI")
    st.markdown("##### Your Safe, Trusted Educational Health Companion for Bangladesh")

with header_col2:
    st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
    language_choice = st.selectbox(
        "Language / ভাষা",
        ["English", "Bangla (বাংলা)"],
        label_visibility="collapsed"
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# Dynamic UI labels
if language_choice == "Bangla (বাংলা)":
    subtitle_text = "ওষুধের ব্যবহার, সাধারণ মাত্রা এবং স্বাস্থ্য সচেতনতা সম্পর্কিত নির্ভরযোগ্য তথ্য জেনে নিন।"
    search_label = "🔍 আপনার স্বাস্থ্য বা ওষুধ সংক্রান্ত প্রশ্ন এখানে লিখুন (বাংলা বা ইংরেজিতে):"
    guidance_title = "📋 শিক্ষণীয় পরামর্শ"
    safety_text = "⚠️ **সতর্কতা:** যেকোনো ওষুধ সেবন করার পূর্বে অবশ্যই বাংলাদেশের একজন রেজিস্টার্ড এমবিবিএস ডাক্তার বা ফার্মাসিস্টের পরামর্শ নিন।"
    topics_title = "💡 সাধারণ স্বাস্থ্য বিষয়সমূহ (ক্লিক করুন):"
else:
    subtitle_text = "Get instant, reliable educational information about common medicines, standard usages, and safety guidelines."
    search_label = "🔍 Type your health or medicine question below (English, Bangla, or Banglish):"
    guidance_title = "📋 Educational Guidance"
    safety_text = "⚠️ **Safety Notice:** Always consult a registered MBBS doctor or pharmacist in Bangladesh before taking any medication."
    topics_title = "💡 Quick Health Topics (Click to Check):"

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
    
    st.markdown(f"#### {topics_title}")
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

    st.markdown("<br>", unsafe_allow_html=True)

    user_query = st.text_input(search_label, value=selected_query, label_visibility="visible")

    if user_query and api_key:
        with st.spinner("Analyzing safely..." if language_choice == "English" else "বিশ্লেষণ করা হচ্ছে..."):
            try:
                client = genai.Client(api_key=api_key)
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

        st.markdown("<br>", unsafe_allow_html=True)
        st.warning(safety_text)

with tab2:
    st.markdown("### 💬 Free Doctor Consultation (Community Queue)")
    st.markdown("""
    *Connect with on-duty volunteer medical students and general practitioners for basic case reviews.*
    
    * **Status:** 🚧 **Coming Soon** — We are onboarding verified doctors and medical volunteers in Bangladesh.
    * **How it will work:** Submit your case history and reports here to enter the community consultation queue for preliminary evaluation.
    """)
    st.info("Stay tuned! This feature will go live as soon as our initial doctor network partnerships are finalized.")

with tab3:
    st.markdown("### ⭐ Paid Expert Consultation (Specialist Booking)")
    st.markdown("""
    *Book direct video appointments or priority text chats with verified specialist physicians (Cardiologists, Pediatricians, etc.).*
    
    * **Status:** 🚧 **Coming Soon** — Integrated bKash/Nagad payment gateways and secure video scheduling are under development.
    * **Benefits:** Guaranteed rapid response times, prescription generation by certified specialists, and direct follow-up chats.
    """)
    st.success("Doctor applications and partnership onboarding will open during Phase 2 of our launch roadmap!")
