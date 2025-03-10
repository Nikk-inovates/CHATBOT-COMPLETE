import faiss
import numpy as np
import pickle
import os
from sentence_transformers import SentenceTransformer

# Define correct paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_FOLDER = os.path.join(BASE_DIR, "data", "processed")
VECTOR_DB_PATH = os.path.join(PROCESSED_FOLDER, "faiss_index")
METADATA_PATH = os.path.join(PROCESSED_FOLDER, "faiss_index_metadata.pkl")

model = SentenceTransformer("all-MiniLM-L6-v2")

def load_faiss_index():
    if not os.path.exists(VECTOR_DB_PATH) or not os.path.exists(METADATA_PATH):
        return None, None

    index = faiss.read_index(VECTOR_DB_PATH)
    with open(METADATA_PATH, "rb") as f:
        text_data = pickle.load(f)

    return index, text_data

def search_faiss(query, k=3):
    index, text_data = load_faiss_index()
    if index is None or text_data is None:
        return ["⚠️ No knowledge base found."]

    query_vector = model.encode([query]).astype(np.float32)
    distances, indices = index.search(query_vector, k)
    return [text_data[i] for i in indices[0] if 0 <= i < len(text_data)]
