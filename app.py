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

st.title("🌸 Sowmya's Study Buddy - With Answers!")
st.write("it will also show the correct answers now!")

uploaded_file = st.file_uploader("upload the pdf", type="pdf")

if uploaded_file:
    reader = PyPDF2.PdfReader(uploaded_file)
    raw_text = ""
    for p in reader.pages:
        t = p.extract_text()
        if t: raw_text += t + " "

    cleaned = raw_text.replace("Scanned by CamScanner", "")
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    sentences = [s.strip() for s in re.split(r'[.!?]', cleaned) if len(s.strip()) > 30]
    sentences = [s for s in sentences if "CamScanner" not in s]

    if len(sentences) < 3:
        st.error("there is less content in the pdf!")
    else:
        st.success("I have read the pdf ✅")
        st.header("📝 Summary")
        st.info(". ".join(sentences[:5]) + ".")

        st.header("🧠 Quiz - 12 Questions with Correct Answer")

        score = 0
        quiz_pool = (sentences * 3)[:12]
        random.shuffle(quiz_pool)

        for i in range(12):
            real_sentence = quiz_pool[i]
            st.subheader(f"Q{i+1}. What does this mean? '{real_sentence[:100]}...'")

            correct = real_sentence[:80] + "..."
            other = [s[:80]+"..." for s in sentences if s!= real_sentence]
            random.shuffle(other)
            wrong_opts = other[:3]
            all_options = [correct] + wrong_opts
            random.shuffle(all_options)

            ans = st.radio(f"Answer for Q{i+1}", all_options, key=f"ans{i}", index=None)

            if ans:
                if ans == correct:
                    st.success("✅ Correct! Super Sowmya! 🎉")
                else:
                    st.error(f"❌ Wrong! Correct answer is: **{correct}**")
                    st.info(f"Explanation: PDF lo '{real_sentence}' ani undi.")
            st.divider()

        st.balloons()
else:
    st.info("upload your pdf!")
