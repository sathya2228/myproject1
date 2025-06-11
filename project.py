import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF
import os

# Gemini API Key Setup
genai.configure(api_key="AIzaSyCYRIxWVAObbS_vcvmvbj13qCu6iaA4dHA")

# Load Gemini model
model = genai.GenerativeModel("gemini-2.0-flash-lite")
# Extract text from PDF or text file
def extract_text(file):
    if file.type == "application/pdf":
        doc = fitz.open(stream=file.read(), filetype="pdf")
        return "\n".join([page.get_text() for page in doc])
    elif file.type == "text/plain":
        return file.read().decode("utf-8")
    else:
        return None

# Streamlit UI
st.set_page_config(page_title="Chat with Your Notes", layout="centered")
st.title("💬 Chat with Your Notes")
st.markdown("Upload your notes and ask questions. Gemini will answer based only on your notes.")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

if uploaded_file:
    with st.spinner("Extracting text..."):
        doc_text = extract_text(uploaded_file)

    if doc_text:
        st.success("Text extracted successfully.")
        st.text_area("Extracted Text Preview", doc_text[:1000] + "...", height=200)

        # User query
        query = st.text_input("Ask a question about your notes")

        if query:
            with st.spinner("Generating response..."):
                prompt = f"""You are an assistant. Answer the following question based *only* on the content below:

                --- DOCUMENT START ---
                {doc_text}
                --- DOCUMENT END ---

                Question: {query}
                Answer:"""

                response = model.generate_content(prompt)
                st.markdown("### ✨ Gemini's Answer")
                st.write(response.text)
    else:
        st.error("Unsupported file type or unable to extract text.")