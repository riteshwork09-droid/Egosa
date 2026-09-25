import json

with open("data/football_data.json", encoding="utf-8") as f:
    data = json.load(f) 

print(data[0])
print(len(data))

from sentence_transformers import SentenceTransformer

texts = [d["text"] for d in data ]

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(texts)

print(embeddings.shape)

import faiss
import numpy as np

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))

faiss.write_index(index, "data/football.index")

print("Index save with", index.ntotal, "enteries")
