import streamlit as st
import PyPDF2
import random
import re

st.set_page_config(page_title="Study Buddy - Sowmya", page_icon="📚")

st.markdown("""
<style>
.stApp {
    background-color: #ffe4ec;
}
.stApp p, .stApp div, .stApp label, .stApp span, .stApp li {
    color: #000000 !important;
}
h1, h2, h3 {
    color: #b4004e !important;
}
</style>
""", unsafe_allow_html=True)

st.title("📚 Sowmya's SUPER Study Buddy!")
st.write("PDF upload chey - Summary + Quiz ostundi! 💖")

uploaded_file = st.file_uploader("PDF ikkada pettu", type="pdf")

if uploaded_file:
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        t = page.extract_text()
        if t:
            text += t + "\n"
    st.success(f"i have studied! {len(reader.pages)} pages 💖")
    tab1, tab2, tab3 = st.tabs(["📄 Full Text", "✨ Summary", "📝 Quiz"])
    with tab1:
        st.text_area("Content", text[:8000], height=400)
    with tab2:
        st.subheader("5 Points Summary:")
        sents = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.strip()) > 30]
        for i, s in enumerate(sents[:5], 1):
            st.write(f"**{i}.** {s}.")
    with tab3:
        st.subheader("Quiz!")
        sents = [s.strip() for s in re.split(r'[.!?]+', text) if 20 < len(s.strip()) < 150]
        if len(sents) >= 3:
            for i, s in enumerate(random.sample(sents, 3), 1):
                st.write(f"**Q{i}:** {s}")
                st.radio(f"Answer Q{i}", ["Correct", "Wrong", "i dont know"], key=f"q{i}", horizontal=True)
            if st.button("Submit"):
                st.balloons()
                st.success("Super Sowmya! Quiz Done! 🎉💖")
else:
    st.warning("upload your pdf Sowmya 💖")
