import os
import shutil
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from load_docs import load_all_can2025_data

# Initialisation du modèle d'embedding
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def create_vector_db():
    # Appel de votre fonction telle qu'elle est nommée dans load_docs.py
    chunks = load_all_can2025_data()
    
    if not chunks:
        print("⚠️ Aucun document trouvé. Vérifiez vos fichiers JSON et votre config.")
        return

    # Gestion du dossier de l'index
    if os.path.exists("faiss_index_can2025"):
        shutil.rmtree("faiss_index_can2025")

    print("🧠 Création de l'index FAISS en cours...")
    # Création de la base de données vectorielle à partir de vos chunks
    vector_db = FAISS.from_documents(chunks, embedding_model)
    
    # Sauvegarde locale
    vector_db.save_local("faiss_index_can2025")
    print("💾 Indexation terminée avec succès !")

if __name__ == "__main__":
    create_vector_db()
    