import streamlit as st
from pdf_reader import extract_text_from_pdf
from summarizer import (
    summarize_text,
    extract_keypoints,
    extract_keywords,
    translate_summary,
    chat_with_document
)

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Content Summarizer",
    page_icon="📝",
    layout="wide"
)

# ---------------- SESSION STATE ----------------

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "keypoints" not in st.session_state:
    st.session_state.keypoints = ""

if "keywords" not in st.session_state:
    st.session_state.keywords = ""

if "translation" not in st.session_state:
    st.session_state.translation = ""

if "document_text" not in st.session_state:
    st.session_state.document_text = ""

# ---------------- TITLE ----------------

st.title("📝 AI Content Summarizer")

st.caption(
    "Upload PDFs, Generate Summaries, Extract Insights & Chat with Documents"
)

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.header("⚙️ Settings")

    summary_type = st.selectbox(
        "Summary Length",
        [
            "Short",
            "Medium",
            "Detailed"
        ]
    )

    language = st.selectbox(
        "Output Language",
        [
            "English",
            "Hindi",
            "Hinglish"
        ]
    )

    st.markdown("---")

    st.success("Groq Llama Connected")

# ---------------- INPUT SECTION ----------------

uploaded_file = st.file_uploader(
    "📄 Upload PDF",
    type=["pdf"]
)

manual_text = st.text_area(
    "📝 Paste Content",
    height=250
)

# ---------------- GENERATE BUTTON ----------------

if st.button(
    "🚀 Generate AI Analysis",
    use_container_width=True
):

    # PDF Upload
    if uploaded_file is not None:

        with st.spinner("Reading PDF..."):

            text = extract_text_from_pdf(
                uploaded_file
            )

        st.success(
            "PDF Processed Successfully!"
        )

    else:

        text = manual_text

    # Empty Check
    if text:

        st.session_state.document_text = text

        # Metrics
        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Words",
                len(text.split())
            )

        with col2:

            st.metric(
                "Characters",
                len(text)
            )

        # AI Processing
        with st.spinner(
            "Analyzing Content..."
        ):

            st.session_state.summary = (
                summarize_text(
                    text,
                    summary_type
                )
            )

            st.session_state.keypoints = (
                extract_keypoints(
                    text
                )
            )

            st.session_state.keywords = (
                extract_keywords(
                    text
                )
            )

            st.session_state.translation = (
                translate_summary(
                    text,
                    language
                )
            )

    else:

        st.warning(
            "Please upload a PDF or paste some content."
        )

# ---------------- TABS ----------------

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📄 Summary",
        "🎯 Key Points",
        "🔑 Keywords",
        "🌍 Language Summary",
        "🤖 Chat With PDF"
    ]
)

# ---------------- SUMMARY ----------------

with tab1:

    st.write(
        st.session_state.summary
    )

    if st.session_state.summary:

        st.download_button(
            "📥 Download Summary",
            st.session_state.summary,
            file_name="summary.txt",
            mime="text/plain"
        )

# ---------------- KEY POINTS ----------------

with tab2:

    st.write(
        st.session_state.keypoints
    )

    if st.session_state.keypoints:

        st.download_button(
            "📥 Download Key Points",
            st.session_state.keypoints,
            file_name="keypoints.txt",
            mime="text/plain"
        )

# ---------------- KEYWORDS ----------------

with tab3:

    st.write(
        st.session_state.keywords
    )

    if st.session_state.keywords:

        st.download_button(
            "📥 Download Keywords",
            st.session_state.keywords,
            file_name="keywords.txt",
            mime="text/plain"
        )

# ---------------- TRANSLATION ----------------

with tab4:

    st.write(
        st.session_state.translation
    )

    if st.session_state.translation:

        st.download_button(
            "📥 Download Translation",
            st.session_state.translation,
            file_name="translation.txt",
            mime="text/plain"
        )

# ---------------- CHAT WITH PDF ----------------

with tab5:

    st.subheader(
        "🤖 Chat With Your Document"
    )

    question = st.chat_input(
        "Ask anything about your PDF..."
    )

    if question:

        answer = chat_with_document(
            st.session_state.document_text,
            question
        )

        st.chat_message(
            "user"
        ).write(question)

        st.chat_message(
            "assistant"
        ).write(answer)
