import streamlit as st
import PyPDF2
import random
import re

st.set_page_config(page_title="united minds Study Buddy", page_icon="📚")
st.markdown("<style>.stApp{background-color:#ffe4ec!important;} h1,h2{color:#b4004e!important;} p,label{color:#000!important;}</style>", unsafe_allow_html=True)

st.title("🌸 united minds Study Buddy - FINAL")

uploaded_file = st.file_uploader("upload your pdf", type="pdf")

if uploaded_file:
    # Only one time read PDF - save in session
    if "quiz_ready" not in st.session_state or st.session_state.get("file_name")!= uploaded_file.name:
        reader = PyPDF2.PdfReader(uploaded_file)
        raw = ""
        for p in reader.pages:
            t = p.extract_text()
            if t: raw += t + " "

        cleaned = raw.replace("Scanned by CamScanner","")
        cleaned = re.sub(r'\s+',' ',cleaned)
        sentences = [s.strip() for s in re.split(r'[.!?]', cleaned) if len(s.strip())>30]
        sentences = [s for s in sentences if "CamScanner" not in s]

        st.session_state.sentences = sentences
        st.session_state.summary = ". ".join(sentences[:5]) + "."

        # Create 12 quiz FIXED one time only
        quiz_data = []
        pool = (sentences*3)[:12]
        for i in range(12):
            real = pool[i] if i < len(pool) else sentences[i%len(sentences)]
            correct = real[:100]
            other = [s[:100] for s in sentences if s!=real]
            random.shuffle(other)
            opts = [correct] + other[:3]
            random.shuffle(opts)
            quiz_data.append({"q": real[:120]+"...?", "correct": correct, "options": opts})

        st.session_state.quiz_data = quiz_data
        st.session_state.file_name = uploaded_file.name
        st.session_state.quiz_ready = True

    st.success("PDF Ready ✅")
    st.header("📝 Summary")
    st.info(st.session_state.summary)

    st.header("🧠 Quiz - 12 Questions (Fixed!)")
    st.write("one questioon answered,another doesn't change now!")

    for i, qitem in enumerate(st.session_state.quiz_data):
        st.subheader(f"Q{i+1}. {qitem['q']}")
        ans = st.radio(f"Select Q{i+1}", qitem["options"], key=f"final_fix_q{i}", index=None)
        if ans:
            if ans == qitem["correct"]:
                st.success(f"✅ CORRECT! united minds super! 🎉")
            else:
                st.error(f"❌ Wrong! Correct is: {qitem['correct']}")
        st.divider()

    if st.button("🔄 New Quiz - Same PDF tho malli"):
        del st.session_state.quiz_ready
        st.rerun()

else:
    st.info("upload your pdf!")
