import os
import torch
from google import genai
import chromadb
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

# -- env variables -----------------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
CHROMA_PATH    = os.getenv("CHROMA_PATH", "./chroma_data")

# -- embedding model ---------------------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"

if device == "cuda":
    print(f"GPU detected: {torch.cuda.get_device_name(0)}")
else:
    print("No GPU detected, running on CPU (slower)")

embedding_model = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2",
    device=device
)

# -- gemini client -----------------------------------------
client=genai.Client(api_key=GEMINI_API_KEY)

# -- chromadb client + collections ------------------------
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

cv_collection = chroma_client.get_or_create_collection(
    name="cv_vectors",
    metadata={"hnsw:space": "cosine"}
)

job_collection = chroma_client.get_or_create_collection(
    name="job_vectors",
    metadata={"hnsw:space": "cosine"}
)