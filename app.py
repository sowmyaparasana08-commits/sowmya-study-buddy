import streamlit as st
import PyPDF2
import random
import re

st.set_page_config(page_title="Study Buddy - Sowmya", page_icon="📚")

st.markdown("""
<style>
.stApp { background-color: #ffe4ec; }
.stApp p, .stApp div, .stApp label, .stApp span, .stApp li { color: #000000 !important; }
h1, h2, h3 { color: #b4004e !important; }
</style>
""", unsafe_allow_html=True)

st.title("🌸 Sowmya's SUPER Study Buddy!")
st.write("PDF upload chey - Summary + 12 Questions ostundi! 📖")

uploaded_file = st.file_uploader("PDF ikkada pettu", type="pdf")

if uploaded_file:
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        t = page.extract_text()
        if t: text += t + "\n"
    
    if text:
        st.success("I have studied the pdf! ✅")
        st.header("📝 Summary")
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        st.write(". ".join(sentences[:8]) + ".")
        
        st.header("🧠 Quiz - 12 Questions (10-15)")
        quiz_count = 12
        for i in range(1, quiz_count + 1):
            if sentences:
                base = sentences[random.randint(0, len(sentences)-1)][:90]
            else:
                base = text[:90]
            st.subheader(f"Q{i}. What is main idea of: '{base}...'?")
            options = [f"Option A - Q{i}", f"Option B - Correct (from PDF)", f"Option C - Q{i}", f"Option D - Q{i}"]
            random.shuffle(options)
            st.radio(f"Answer for Q{i}", options, key=f"q{i}")
            st.write("---")
        st.balloons()
        st.success(f"Total {quiz_count} questions ready! 🔥")
    else:
        st.error("PDF lo text ledu!")
