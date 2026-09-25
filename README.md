# ⚽ Egosa — Football RAG Chatbot

Egosa is a domain-restricted chatbot that answers questions about **La Liga, Premier League, and Champions League** football only. It's built using **RAG (Retrieval-Augmented Generation)** — instead of relying on an LLM's built-in knowledge, it retrieves facts from a custom knowledge base before generating an answer.

**Live demo:** [https://egosa-chatbot.streamlit.app/](https://egosa-chatbot.streamlit.app/)

## Why this project

Egosa stays strictly within its football domain, but rather than being limited to a small hand-curated dataset, it prefers verified facts when available and falls back to general football knowledge otherwise — while staying honest when it isn't confident.

## How it works

```
User question
      ↓
Topic guardrail (keyword check across current message + conversation history)
      ↓
Query → embedded into a vector (sentence-transformers)
      ↓
FAISS searches the knowledge base for the most relevant facts
      ↓
Retrieved facts + conversation history + question → sent to Gemini as context
      ↓
LLM answers using retrieved facts first, general football knowledge as fallback
```

## Tech stack

| Piece | Tool | Why |
|---|---|---|
| Knowledge base | JSON | Simple, structured, easy to grow |
| Embeddings | `sentence-transformers` (`all-MiniLM-L6-v2`) | Free, local, fast — turns text into vectors by meaning |
| Vector search | FAISS | Fast similarity search over embeddings |
| LLM | Google Gemini | Generates the final natural-language answer |
| UI | Streamlit | Chat interface, deployed to Streamlit Community Cloud |

## Project structure

```
egosa/
├── data/
│   ├── football_data.json   # knowledge base
│   └── football.index       # saved FAISS index (generated)
├── ingest.py                 # builds embeddings + FAISS index
├── retriever.py                # retrieves top-k relevant facts for a query
├── chatbot.py                    # guardrail + retrieval + conversation memory + LLM call
├── app.py                          # Streamlit UI
└── requirements.txt
```

## Running it locally

```bash
git clone https://github.com/riteshwork09-droid/Egosa.git
cd Egosa
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Create a `.env` file in the project root:
```
GEMINI_API_KEY=your-key-here
```

Build the index (only needed once, or after changing `football_data.json`):
```bash
python ingest.py
```

Run the app:
```bash
streamlit run app.py
```

## Design decisions

- **Topic guardrail runs before retrieval** — off-topic questions are rejected immediately, without spending an API call or search.
- **Guardrail checks conversation history, not just the current message** — so follow-up questions like "why not X instead" are correctly understood as still on-topic, based on earlier messages in the same session.
- **The LLM prefers retrieved context but can fall back to general knowledge** — this is a deliberate trade-off between strict grounding (safer, but limited to dataset coverage) and broader usefulness (better coverage, slightly less strictly verified).
- **FAISS `IndexFlatL2`** was chosen for exact search at this dataset's small scale; a larger dataset would move to an approximate index (`IndexIVFFlat` / `HNSW`) for speed.

## Known limitations / next steps

- Keyword-based guardrail is still an approximation — very indirect follow-ups deep into a conversation may occasionally be misclassified.
- Free-tier Gemini API has a daily request quota (20 requests/day on the model used here) — heavy testing can hit this limit; a production version would need a paid tier or rate-limit handling with graceful fallback messaging.
- Knowledge base currently has a small number of entries — coverage is limited outside trophies/records/player facts covered directly; general questions fall back to the LLM's own knowledge.
- Planned: expand dataset, add live data via a football API, explore tool-use/agentic features (e.g. generating study-plan-style PDFs) as a separate follow-up project.

## Author

Built by Ritesh as a hands-on project to learn RAG, vector search, conversation memory, and LLM application development end-to-end — from data to a deployed product.