# 📄 Resume AI Extractor & HR Assistant

## 🔍 Overview

This project is an AI-powered backend system that extracts structured information from resumes/CVs using Large Language Models (LLMs). It also includes an HR assistant chatbot that helps evaluate and rank candidates based on natural language queries.

---

## 🚀 Features

- Upload multiple resumes (PDF/DOCX)
- Extracts:
  - First Name, Last Name
  - Email Address, Phone Number
  - Education History
  - Work Experience Summary
  - Skills
  - Current Position
  - Total Years of Experience
- Saves parsed data into a FAISS vector store
- Chatbot answers HR-style queries like:
  - “Who is most skilled in Python?”
  - “Rank candidates for a Full Stack Developer role.”

---

## 🛠 Technology Stack

- Python
- Flask
- LangChain + Gemini Pro
- FAISS
- HTML/CSS/JS (basic)

---

## 🧱 AI Architecture Diagram

![AI Architecture Diagram](https://drive.google.com/uc?id=YOUR_ARCHITECTURE_IMAGE_ID)

---

## 📂 Project Structure

├── app.py ├── extract.py ├── chatbot.py ├── database/ ├── temp/ ├── static/ ├── templates/ │ └── index.html ├── .env ├── requirements.txt └── README.md

yaml
Copy
Edit

---

## 🧪 Sample Questions

1. Who is the most skilled in Python coding?
2. Rank the candidates for an AI role.
3. Which candidate has the strongest full-stack development background?
4. Who has the most leadership experience?

---

## 🖼 Screenshots

### Resume Extraction View

![Upload and Results](https://drive.google.com/uc?id=YOUR_SCREENSHOT_ID_1)

### HR Chatbot in Action

![Chatbot Answer](https://drive.google.com/uc?id=YOUR_SCREENSHOT_ID_2)

---

## 🎥 Demo Video

📺 [Watch on Google Drive](https://drive.google.com/file/d/YOUR_VIDEO_ID/view?usp=sharing)

---

## 🧾 Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/resume-ai-extractor.git
   cd resume-ai-extractor
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Create a .env file:

ini
Copy
Edit
GOOGLE_API_KEY=your_google_gemini_api_key
Run the server:

bash
Copy
Edit
python app.py
Open http://127.0.0.1:5000 in your browser

❗ Assumptions & Limitations
Role tags are inferred via LLM prompts

Only PDF/DOCX supported

LLM accuracy depends on resume structure

🔮 Future Improvements
Add multilingual support

Enhance role tagging logic

Integrate real-time memory in chatbot

Link with external ATS systems