import pandas as pd
import re
import os
import pickle
from tqdm import tqdm
import torch

# ===== CONFIG =====
CSV_FILES = [
    "recipes_w_search_terms.csv",  # csv path
    "recipes.csv"
]
OUTPUT_PKL = "domain_vocab.pkl"
USE_GPU = torch.cuda.is_available()
DEVICE = "cuda" if USE_GPU else "cpu"

# ===== FUNCTION TO CLEAN & TOKENIZE =====
def tokenize_text(text: str) -> list[str]:
    """Extract lowercase alphabetic words from text"""
    if not isinstance(text, str):
        return []
    return re.findall(r"[A-Za-z]+", text.lower())

# ===== BUILD VOCAB =====
domain_vocab = set()

for csv_file in CSV_FILES:
    print(f"Processing {csv_file} ...")
    df = pd.read_csv(csv_file)
    
    for col in tqdm(df.columns, desc="Columns", unit="col"):
        for val in tqdm(df[col].dropna().astype(str), desc=f"Rows in {col}", unit="row", leave=False):
            tokens = tokenize_text(val)
            domain_vocab.update(tokens)

print(f"Total unique words in vocab: {len(domain_vocab)}")

# ===== SAVE TO PICKLE =====
with open(OUTPUT_PKL, "wb") as f:
    pickle.dump(domain_vocab, f)

print(f"Saved domain vocab to {OUTPUT_PKL}")

# ===== OPTIONAL: Precompute embeddings on GPU =====
try:
    from sentence_transformers import SentenceTransformer
    print(f"Loading SentenceTransformer model on {DEVICE} ...")
    model = SentenceTransformer("all-MiniLM-L6-v2", device=DEVICE)

    vocab_list = list(domain_vocab)
    batch_size = 512
    embeddings = []

    print("Computing embeddings for domain vocab ...")
    for i in tqdm(range(0, len(vocab_list), batch_size), desc="Batches"):
        batch = vocab_list[i:i+batch_size]
        emb = model.encode(batch, convert_to_tensor=True, device=DEVICE)
        embeddings.append(emb)

    embeddings = torch.cat(embeddings)
    torch.save(embeddings, "domain_vocab_embeddings.pt")
    print("Saved embeddings to domain_vocab_embeddings.pt")
except Exception as e:
    print("Skipping embeddings precomputation:", e)
