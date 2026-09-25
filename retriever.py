import json 
import faiss
from sentence_transformers import SentenceTransformer

with open ("data/football_data.json") as f :
    data = json.load(f)

index = faiss.read_index("data/football.index")
model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve(query, k=3):
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, k)
    results = [data[i]["text"] for i in indices[0]]
    return results

if __name__ == "__main__":
    question = "who won the most champions league titles"
    results = retrieve(question)
    for r in results:
        print(r)
