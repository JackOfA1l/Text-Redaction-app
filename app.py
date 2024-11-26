import streamlit as st
import spacy
import re
import subprocess
import sys

# Function to ensure spaCy model is installed
def load_spacy_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        return spacy.load("en_core_web_sm")

# Load spaCy model
nlp = load_spacy_model()

# Function to redact sensitive information using regex and NER
def redact_text(input_text):
    # Regular expression patterns for sensitive information
    patterns = {
        "email": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        "phone": r'\+?\d{1,4}?\s?\(?\d{1,3}?\)?\s?\d{1,3}[\s.-]?\d{1,3}[\s.-]?\d{1,4}',
        "credit_card": r'\b(?:\d[ -]*?){13,16}\b',
    }

    # Apply regex redaction
    redacted_text = input_text
    for key, pattern in patterns.items():
        redacted_text = re.sub(pattern, '[REDACTED]', redacted_text)

    # Apply NER for names and addresses
    doc = nlp(redacted_text)
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "GPE", "LOC", "ORG"]:  # NER labels for names and addresses
            redacted_text = redacted_text.replace(ent.text, '[REDACTED]')

    return redacted_text

# Streamlit app interface
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        color: #4A90E2;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        text-align: center;
        font-size: 1.2rem;
        color: #6c757d;
        margin-bottom: 2rem;
    }
    .footer {
        text-align: center;
        margin-top: 2rem;
        color: #6c757d;
        font-size: 0.9rem;
    }
    </style>
    <div>
        <h1 class="main-title">🔒 Text Redaction Tool</h1>
        <p class="sub-title">Safeguard sensitive information with regex and AI-powered NER</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Input section
st.markdown("### ✍️ Enter Your Text Below:")
input_text = st.text_area("", height=200, placeholder="Type or paste your text here...")

# Redact button
if st.button("🚀 Redact Sensitive Information"):
    if input_text:
        redacted_result = redact_text(input_text)
        # Display results
        st.markdown("### ✨ Redacted Text:")
        st.success(redacted_result)
    else:
        st.warning("⚠️ Please enter some text to redact.")

# Footer section
st.markdown(
    """
    <div class="footer">
        Made with ❤️ using Streamlit and spaCy
    </div>
    """,
    unsafe_allow_html=True,
)
