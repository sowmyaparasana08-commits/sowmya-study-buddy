import streamlit as st
import PyPDF2
import random
import re

st.set_page_config(page_title="united minds Study Buddy", page_icon="📚")
st.markdown("<style>.stApp{background-color:#ffe4ec!important;} h1,h2{color:#b4004e!important;} p,label{color:#000!important;}</style>", unsafe_allow_html=True)

st.title("🌸 united minds Study Buddy - Final")

# Score dict first lo create
if "answers" not in st.session_state:
    st.session_state.answers = {}

uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

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

        if len(sentences) == 0:
            sentences = ["This is a sample sentence for quiz generation."] * 12

        st.session_state.sentences = sentences
        st.session_state.summary = ". ".join(sentences[:5]) + "."

        quiz_data = []
        for i in range(12):
            real = sentences[i % len(sentences)]
            correct = real[:100]
            other = [s[:100] for s in sentences if s!= real]
            random.shuffle(other)
            opts = [correct] + other[:3]
            random.shuffle(opts)
            quiz_data.append({"q": real[:120]+"?", "correct": correct, "options": opts})

        st.session_state.quiz_data = quiz_data
        st.session_state.file_name = uploaded_file.name
        st.session_state.quiz_ready = True
        st.session_state.answers = {}

    # SCORE CARD - BUG FIXED
    total_q = len(st.session_state.quiz_data)
    total_answered = len(st.session_state.answers)
    correct_count = sum(1 for v in st.session_state.answers.values() if v == True)

    if total_answered > 0:
        st.header("🏆 SCORE CARD")
        col1, col2, col3 = st.columns(3)
        col1.metric("Answered", f"{total_answered}/{total_q}")
        col2.metric("Correct", f"{correct_count}")
        score_per = int(correct_count / total_answered * 100) if total_answered > 0 else 0
        col3.metric("Score", f"{score_per}%")
        st.progress(total_answered / total_q)
        if total_answered == total_q:
            st.balloons()
            if correct_count >= 9:
                st.success(f"🎉 WOW united minds! {correct_count}/{total_q} - You are a Topper!")
            elif correct_count >= 6:
                st.info(f"👏 Good Job united minds! {correct_count}/{total_q}")
            else:
                st.warning(f"💪 Try Again united minds! {correct_count}/{total_q}")

    st.header("📝 Summary")
    st.info(st.session_state.summary)

    st.header("🧠 Quiz - 12 Questions")
    for i, qitem in enumerate(st.session_state.quiz_data):
        st.subheader(f"Q{i+1}. {qitem['q']}")
        ans = st.radio(f"Select Q{i+1}", qitem["options"], key=f"final_q{i}", index=None)
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
    st.info("Please upload a PDF united minds!")
