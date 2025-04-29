import streamlit as st
import pandas as pd
import json
from extract import extract_text_from_pdf, split_text, extract_resume_details, score_candidate_for_ai, add_candidate_to_vectorstore
from chatbot import chatbot_answer
from pathlib import Path
import os

st.set_page_config(page_title="Resume AI Extractor", layout="wide")

st.title("📄 Resume Extractor & HR Assistant")

if "resume_data" not in st.session_state:
    st.session_state.resume_data = []

uploaded_files = st.file_uploader("Upload Resume(s)", type=["pdf", "docx"], accept_multiple_files=True)

if st.button("Extract Resumes"):
    if uploaded_files:
        for pdf in uploaded_files:
            st.markdown(f"### Extracting: {pdf.name}")
            raw_text = extract_text_from_pdf([pdf])
            
            try:
                extracted_json = extract_resume_details(raw_text)
                extracted_json["ai_skill_score"] = score_candidate_for_ai(extracted_json)
                st.session_state.resume_data.append(extracted_json)
                add_candidate_to_vectorstore(extracted_json)  
            except Exception as e:
                st.error(f"Error processing {pdf.name}: {str(e)}")
        
        st.success("Extraction and Embedding completed!")
    else:
        st.warning("Please upload some resumes first.")

if st.session_state.resume_data:
    st.markdown("## 🧾 Extracted Details")
    
    for idx, resume in enumerate(st.session_state.resume_data):
        with st.expander(f"📄 Resume {idx+1}: {resume.get('First Name', '')} {resume.get('Last Name', '')}", expanded=True):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("### 🔍 Basic Info")
                st.markdown(f"**📧 Email:** {resume.get('Email Address', 'Not Available')}")
                st.markdown(f"**📱 Phone:** {resume.get('Phone Number', 'Not Available')}")
                
                st.markdown("### 🎓 Education")
                edu_text = resume.get('Education History', 'Not Available')
                st.markdown(edu_text)

            with col2:
                st.markdown("### 💼 Career Overview")
                st.markdown(f"**🏢 Current Position:** {resume.get('Current Position', 'Not Available')}")
                st.markdown(f"**📅 Years of Experience:** {resume.get('Total Years of Experience', 'Not Available')}")
                
                st.markdown("### 🛠 Skills")
                skills_text = resume.get('Skills', 'Not Available')
                st.markdown(f"```\n{skills_text}\n```")
                
                st.markdown("### 📈 Work Experience")
                exp_text = resume.get('Work Experience Summary', 'Not Available')
                st.markdown(exp_text)
        
        st.markdown("---")

st.markdown("## 🤖 HR Chatbot")

query = st.text_input("Ask a question (e.g., Who is the best Python developer?)")

if st.button("Ask"):
    if query:
        with st.spinner("Thinking..."):
            response = chatbot_answer(query)
            st.success(response)
    else:
        st.warning("Enter a question first.")
