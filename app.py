import streamlit as st
import PyPDF2
import random
import re

st.set_page_config(page_title="united minds Study Buddy", page_icon="📚")
st.markdown("<style>.stApp{background-color:#ffe4ec!important;} h1,h2{color:#b4004e!important;} p,label{color:#000!important;}</style>", unsafe_allow_html=True)

st.title("🌸 united minds Study Buddy - Final Fixed")

# IMPORTANT - Score dict ni first lo ne create chey
if "answers" not in st.session_state:
    st.session_state.answers = {}

uploaded_file = st.file_uploader("upload your pdf", type="pdf")

if uploaded_file:
    if "quiz_ready" not in st.session_state or st.session_state.get("file_name")!= uploaded_file.name:
        reader = PyPDF2.PdfReader(uploaded_file)
        raw = ""
        for p in reader.pages:
            t = p.extract_text()
            if t: raw += t + " "
        cleaned = raw.replace("Scanned by CamScanner","")
        cleaned = re.sub(r'\s+',' ',cleaned)
        sentences = [s.strip() for s in re.split(r'[.!?]', cleaned) if len(s.strip())>30]
        sentences = [s for s in sentences if "PRACTICE SET" not in s and "Practice Set" not in s and "CamScanner" not in s and len(s.split())>4]

        st.session_state.summary = ". ".join(sentences[:5]) + "."

        quiz_data = []
        for i in range(min(12, len(sentences))):
            real = sentences[i]
            correct = real[:100]
            other = [s[:100] for s in sentences if s!=real]
            random.shuffle(other)
            opts = [correct] + other[:3]
            random.shuffle(opts)
            quiz_data.append({"q": real[:120]+"?", "correct": correct, "options": opts})

        st.session_state.quiz_data = quiz_data
        st.session_state.file_name = uploaded_file.name
        st.session_state.quiz_ready = True
        st.session_state.answers = {} # Reset score for new PDF

    # SCORE CARD
    total_answered = len(st.session_state.answers)
    correct_count = sum(1 for v in st.session_state.answers.values() if v==True)
    if total_answered > 0:
        st.header("🏆 SCORE CARD")
        col1, col2, col3 = st.columns(3)
        col1.metric("Answered", f"{total_answered}/12")
        col2.metric("Correct", f"{correct_count}")
        col3.metric("Score", f"{int(correct_count/max(1,total_answered)*100)}%")
        st.progress(total_answered/12)
        if total_answered == 12:
            st.balloons()
            st.success(f"🎉 Wow united minds! {correct_count}/12 - Topper!")

    st.header("📝 Summary")
    st.info(st.session_state.summary)

    st.header("🧠 Quiz - 12 Questions")
    for i, qitem in enumerate(st.session_state.quiz_data):
        st.subheader(f"Q{i+1}. {qitem['q']}")
        ans = st.radio(f"Select Q{i+1}", qitem["options"], key=f"fixed_q{i}", index=None)
        if ans:
            is_correct = (ans == qitem["correct"])
            st.session_state.answers[i] = is_correct
            if is_correct:
                st.success("✅ CORRECT! Super united minds!")
            else:
                st.error(f"❌ Wrong! Correct is: {qitem['correct']}")
        st.divider()

    if st.button("🔄 New Quiz"):
        st.session_state.answers = {}
        if "quiz_ready" in st.session_state:
            del st.session_state.quiz_ready
        st.rerun()
else:
    st.info("upload your pdf!")
