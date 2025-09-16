import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from app.file_handler import read_file

DATA_DIR = "data"
UPLOAD_DIR = os.path.join(DATA_DIR, "uploaded")
INDEX_DIR = os.path.join(DATA_DIR, "index")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(INDEX_DIR, exist_ok=True)

model = SentenceTransformer("all-MiniLM-L6-v2")

def save_index(index, filepath):
    faiss.write_index(index, filepath)

def load_index(filepath):
    return faiss.read_index(filepath)

def embed_and_save(file_path: str):
    text = read_file(file_path)
    chunks = text.split("\n\n")

    embeddings = model.encode(chunks)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    # Save index + metadata
    file_name = os.path.basename(file_path)
    base_name = os.path.splitext(file_name)[0]

    save_index(index, os.path.join(INDEX_DIR, f"{base_name}.index"))
    with open(os.path.join(INDEX_DIR, f"{base_name}_chunks.pkl"), "wb") as f:
        pickle.dump(chunks, f)

    return base_name
