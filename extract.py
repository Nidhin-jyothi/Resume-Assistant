import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnableSequence
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def extract_text_from_pdf(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def split_text(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=200)
    return splitter.split_text(text)

VECTOR_PATH = "database/faiss_index"

def add_candidate_to_vectorstore(candidate_details: dict):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    text = json.dumps(candidate_details)

    if not os.path.exists(VECTOR_PATH):
        store = FAISS.from_texts([text], embedding=embeddings, metadatas=[candidate_details])
    else:
        store = FAISS.load_local(VECTOR_PATH, embeddings, allow_dangerous_deserialization=True)
        store.add_texts([text], metadatas=[candidate_details])

    store.save_local(VECTOR_PATH)

def extract_resume_details(text):
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.2)
    
    prompt = PromptTemplate(
        input_variables=["resume_text"],
        template="""

        You are an expert resume screener.
        Extract the following fields STRICTLY AS JSON WITHOUT MARKDOWN WRAPPING:

        - First Name
        - Last Name
        - Email Address
        - Phone Number
        - Education History
        - Work Experience Summary(Strictly mentioning all work experience)
        - Skills
        - Current Position
        - Total Years of Experience

        Resume Text:
        {resume_text}

        If a field is missing indiacte Not Available instead of null

        """
    )
    
    chain = prompt | model
    response = chain.invoke({"resume_text": text})

    print("Raw Response:", response.content)

    if not response.content:
        raise ValueError("Error: The model returned an empty response.")

    try:
        parsed_data = json.loads(response.content)
        return parsed_data

    except json.JSONDecodeError as e:
        
        raise ValueError(f"Error parsing extraction: Invalid JSON format - {str(e)}")

    except Exception as e:
        
        raise ValueError(f"Error parsing extraction: {str(e)}")



def score_candidate_for_ai(details: dict) -> dict:
    
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.2)
    prompt = PromptTemplate(
        input_variables=["candidate_json"],
        template="""

        You are an expert recruiter.  
        Given this candidate’s details (in JSON), identify all the professional roles 
        (e.g., “Python Developer”, “AI Developer”, “Data Scientist”, “Backend Engineer”, etc.) 
        for which they would be a good fit.  
        For each role, assign a suitability score from 1 (poor) to 10 (excellent).  

        **Output** ONLY a JSON object with a single field `"role_tags"`, which maps each role name to its integer score.  
        No extra text.

        Candidate Details:
        {candidate_json}

        """
    )
    chain = prompt | model
    
    response = chain.invoke({
        "candidate_json": json.dumps(details)
    })
    return response.content
