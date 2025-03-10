import os
import pdfplumber
import nltk
import re
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
from tqdm import tqdm  # Progress bar

nltk.download("punkt")

# ✅ Define correct paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_FOLDER = os.path.join(BASE_DIR, "data", "documents")  # PDFs stored here
PROCESSED_FOLDER = os.path.join(BASE_DIR, "data", "processed")  # FAISS storage
VECTOR_DB_PATH = os.path.join(PROCESSED_FOLDER, "faiss_index")
METADATA_PATH = os.path.join(PROCESSED_FOLDER, "faiss_index_metadata.pkl")

os.makedirs(PROCESSED_FOLDER, exist_ok=True)  # Ensure processed folder exists

# ✅ Load embedding model
print("🚀 Loading SentenceTransformer model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

def clean_text(text):
    """Remove special characters, extra spaces, and fix encoding issues."""
    text = text.encode("utf-8", "ignore").decode("utf-8")  # Fix broken encodings
    text = re.sub(r"\(cid:\d+\)", "", text)  # Remove (cid:xyz) artifacts
    text = re.sub(r"\s+", " ", text).strip()  # Remove extra spaces
    return text

def extract_text_from_pdfs():
    """Extract text from all PDFs and clean it."""
    text_data = []
    
    if not os.path.exists(DOCS_FOLDER):
        print(f"❌ ERROR: Documents folder '{DOCS_FOLDER}' not found.")
        return []

    pdf_files = [f for f in os.listdir(DOCS_FOLDER) if f.endswith(".pdf")]

    if not pdf_files:
        print("⚠️ WARNING: No PDF files found in 'data/documents/'.")
        return []

    for filename in tqdm(pdf_files, desc="📄 Processing PDFs"):
        pdf_path = os.path.join(DOCS_FOLDER, filename)
        try:
            with pdfplumber.open(pdf_path) as pdf:
                extracted_text = []
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        cleaned_text = clean_text(text)  # 🧹 Clean text
                        extracted_text.append(cleaned_text)

                if extracted_text:
                    text_data.append(" ".join(extracted_text))
                    print(f"✅ Extracted and cleaned text from {filename}")
                else:
                    print(f"⚠️ WARNING: No readable text found in {filename}")

        except Exception as e:
            print(f"❌ ERROR: Failed to read {filename}: {e}")

    return text_data

def split_text_into_chunks(text_data, chunk_size=3):
    """Split text into smaller chunks."""
    chunks = []
    for text in text_data:
        sentences = sent_tokenize(text)
        for i in range(0, len(sentences), chunk_size):
            chunks.append(" ".join(sentences[i:i + chunk_size]))
    return chunks

def create_faiss_index(text_chunks):
    """Create FAISS index."""
    if not text_chunks:
        print("⚠️ WARNING: No text chunks to process. FAISS index was not created.")
        return

    print("⚡ Encoding text into vectors...")
    vectors = model.encode(text_chunks, batch_size=16, show_progress_bar=True)
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(np.array(vectors, dtype=np.float32))

    # ✅ Save FAISS index & metadata
    faiss.write_index(index, VECTOR_DB_PATH)
    with open(METADATA_PATH, "wb") as f:
        pickle.dump(text_chunks, f)

    print("✅ FAISS index created and saved successfully!")

# ✅ Run document processing
if __name__ == "__main__":
    print("📄 Extracting text from PDFs...")
    extracted_text = extract_text_from_pdfs()

    if extracted_text:
        print("📌 Splitting text into chunks...")
        text_chunks = split_text_into_chunks(extracted_text)

        print("🔍 Creating FAISS index...")
        create_faiss_index(text_chunks)

        print("🚀 Documents successfully processed & stored in FAISS!")
    else:
        print("⚠️ No documents were processed. Exiting.")
