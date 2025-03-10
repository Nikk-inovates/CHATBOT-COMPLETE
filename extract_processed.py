import os
import pickle
import faiss
import logging

# ✅ Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ✅ Define paths for processed data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the script's directory
PROCESSED_FOLDER = os.path.join(BASE_DIR, "data", "processed")  # ✅ Ensure processed folder is inside `backend/data/`
VECTOR_DB_PATH = os.path.join(PROCESSED_FOLDER, "faiss_index")
METADATA_PATH = os.path.join(PROCESSED_FOLDER, "faiss_index_metadata.pkl")  # ✅ Ensure this matches the actual filename!

def load_processed_data():
    """Load FAISS index and metadata (processed chunks)."""
    
    if not os.path.exists(VECTOR_DB_PATH) or not os.path.exists(METADATA_PATH):
        logging.error("❌ ERROR: Processed data not found! Run `process_documents.py` first.")
        return None, None

    try:
        # ✅ Load FAISS index
        index = faiss.read_index(VECTOR_DB_PATH)

        # ✅ Load metadata (text chunks)
        with open(METADATA_PATH, "rb") as f:
            text_data = pickle.load(f)

        logging.info("✅ Processed data loaded successfully!")
        return index, text_data

    except Exception as e:
        logging.error(f"❌ ERROR: Failed to load processed data: {e}")
        return None, None

if __name__ == "__main__":
    logging.info("📂 Loading processed FAISS data from 'backend/data/processed'...")
    index, text_chunks = load_processed_data()

    if text_chunks:
        logging.info(f"🚀 Extracted {len(text_chunks)} processed text chunks!")
        print("\n📌 **First 5 Extracted Chunks:**")
        for i, chunk in enumerate(text_chunks[:5], 1):
            print(f"{i}. {chunk}\n")
    else:
        logging.warning("⚠️ No processed data available.")
