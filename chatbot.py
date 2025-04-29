import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

load_dotenv()
VECTOR_PATH = "database/faiss_index"

def load_vector_store():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    return FAISS.load_local(VECTOR_PATH, embeddings, allow_dangerous_deserialization=True)

def chatbot_answer(question: str, role: str = "AI Developer") -> str:
    store = load_vector_store()

    docs = store.similarity_search(question, k=5)

    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.2)
    prompt = PromptTemplate(
        input_variables=["candidates", "question", "role"],
        template="""
        
    You are an expert HR assistant evaluating candidates for the "{role}" role or role if mentioned in the "{question}".

    Here are up to 5 candidate profiles (JSON):
    {candidates}

    Question: {question}

    Analyze candidates for the given role and based on the Question, 
    and give a one-sentence justification for each. 
 
    """
    )
    chain = prompt | model
    response = chain.invoke({
        "candidates": "\n".join(doc.page_content for doc in docs),
        "question": question,
        "role": role
    })
    return response.content
