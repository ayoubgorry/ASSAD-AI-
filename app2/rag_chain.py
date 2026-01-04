import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
app = FastAPI(title="CAN 2025 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # DEV ONLY
    allow_credentials=False,  # IMPORTANT avec *
    allow_methods=["*"],
    allow_headers=["*"],
)
# 1. Configuration des modèles
# IMPORTANT : Doit être identique au script d'indexation
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

llm = ChatGoogleGenerativeAI(
    model="gemini-3-pro-preview",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# 2. Chargement de la base de données
vector_db = FAISS.load_local(
    "faiss_index_can2025", 
    embedding_model, 
    allow_dangerous_deserialization=True
)

# Augmentez le K pour être sûr de couvrir les phases finales si le fichier est fragmenté
retriever = vector_db.as_retriever(
    search_type="similarity", # Plus direct pour les dates/phases spécifiques
    search_kwargs={"k": 20}    # Récupère plus de contexte
)

# 3. Prompt et Chaîne RAG
template = """Tu es un expert de la CAN 2025. Réponds précisément à la question en utilisant le contexte fourni.
Si tu ne sais pas, dis que tu n'as pas l'information.

CONTEXTE :
{context}

QUESTION :
{question}

RÉPONSE :"""

prompt = ChatPromptTemplate.from_template(template)

def format_docs(docs):
    return "\n\n".join(f"--- SOURCE: {d.metadata.get('source')} ---\n{d.page_content}" for d in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 4. API Endpoint
class Question(BaseModel):
    query: str

@app.post("/chat")
async def chat(question: Question):
    try:
        response = rag_chain.invoke(question.query)
        return {"response": response}
    except Exception as e:
        return {"response": f"Erreur serveur : {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)