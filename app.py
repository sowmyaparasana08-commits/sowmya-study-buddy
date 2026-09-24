import streamlit as st
import PyPDF2
import random
import re

st.set_page_config(page_title="Sowmya's Study Buddy", page_icon="📚")
st.markdown("""
<style>
.stApp { background-color: #ffe4ec!important; }
h1,h2,h3 { color: #b4004e!important; }
p, span, label { color: #000!important; }
</style>
""", unsafe_allow_html=True)

st.title("🌸 Sowmya's Study Buddy - FINAL FIXED")
st.write("Scanned text 'CamScanner' the bug is completely gone!")

uploaded_file = st.file_uploader("upload the pdf", type="pdf")

if uploaded_file:
    reader = PyPDF2.PdfReader(uploaded_file)
    raw_text = ""
    for page in reader.pages:
        t = page.extract_text()
        if t: raw_text += t + " "

    # 1. BUG FIX: CamScanner watermark remove
    cleaned = raw_text.replace("Scanned by CamScanner", "")
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()

    # Sentences teeyadam
    sentences = [s.strip() for s in re.split(r'[.!?]', cleaned) if len(s.strip()) > 30]
    sentences = [s for s in sentences if "CamScanner" not in s]

    if len(sentences) < 3:
        st.error("there is less content in the pdf, Sowmya, please send the clear pdf!")
    else:
        st.success("i have studied the pdf ✅")
        st.header("📝 Summary")
        st.info(". ".join(sentences[:5]) + ".")

        st.header("🧠 Quiz - 12 Real Questions from PDF")

        # Real questions from PDF
        quiz_pool = sentences[:12] if len(sentences) >= 12 else (sentences * 3)[:12]
        random.shuffle(quiz_pool)

        for i in range(12):
            real_sentence = quiz_pool[i]
            # Question ni real sentence nundi create chey
            words = real_sentence.split()
            if len(words) > 6:
                q_text = " ".join(words[:8]) + "...? - What comes next?"
            else:
                q_text = real_sentence

            st.subheader(f"Q{i+1}. {q_text}")

            # Correct answer = real sentence
            correct = real_sentence[:80] + "..."
            # Wrong options = vere sentences nundi
            other_sents = [s[:80]+"..." for s in sentences if s!= real_sentence]
            random.shuffle(other_sents)
            wrong_opts = other_sents[:3]

            all_options = [correct] + wrong_opts
            random.shuffle(all_options)

            # Ikkada Option A B ane kaadu, real text vastundi!
            st.radio(f"Select correct continuation for Q{i+1}:", all_options, key=f"final_q{i}", index=None)
            st.divider()

        st.balloons()
        st.success("12 Real PDF Questions Ready! 🎉")
else:
    st.info("upload your pdf!")
