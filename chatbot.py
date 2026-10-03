import os
from datetime import date
from dotenv import load_dotenv
from google import genai
from retriever import retrieve

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

ALLOWED_KEYWORDS = [
    "la liga", "laliga", "premier league", "epl",
    "champions league", "ucl", "football", "soccer","football",
    "messi", "ronaldo", "haaland", "mbappe", "mbappé",
    "bellingham", "vinicius", "vinícius", "yamal",
    "lewandowski", "salah", "benzema", "ballon d'or",
    "real madrid", "barcelona", "manchester city", "manchester united",
    "liverpool", "arsenal", "chelsea", "bayern munich"
]

def is_on_topic(query, history):
    query_lower = query.lower()
    if any(keyword in query_lower for keyword in ALLOWED_KEYWORDS):
        return True

    # Fallback: if recent conversation was on-topic, treat short follow-ups as on-topic too
    recent_text = " ".join(m["content"].lower() for m in history[-10:])
    return any(keyword in recent_text for keyword in ALLOWED_KEYWORDS)

from retriever import retrieve_with_scores

SIMILARITY_THRESHOLD = 1.0  # tune this after testing — lower = stricter

from retriever import retrieve_with_scores

SIMILARITY_THRESHOLD = 1.0

def ask_egosa(query, today = date.today().strftime("%B %d, %Y"), history=None):
    if history is None:
        history = []

    # Combine the current question with recent conversation for a richer topic check
    recent_context = " ".join(m["content"] for m in history[-4:])
    combined_query = f"{recent_context} {query}".strip()

    context_text, best_distance = retrieve_with_scores(combined_query)

    if best_distance >= SIMILARITY_THRESHOLD:
        return "I'm Egosa — I only answer questions about La Liga, Premier League, and Champions League football."

    history_text = ""
    for m in history[-6:]:
        role = "User" if m["role"] == "user" else "Egosa"
        history_text += f"{role}: {m['content']}\n"



    prompt = f"""You are Egosa, a football chatbot for La Liga, Premier League, and Champions League only.
Today's date is {today}. Use this for any date, age, or year calculations — never guess or assume a different year.
You have no verified information about your own creator or developer unless it appears explicitly in the context below. If asked and nothing relevant is in the context, say you don't have that information rather than guessing.
Never invent dates, ages, or biographical facts that aren't explicitly stated in the context.
First, try to answer using the context below, since it's verified information.
If the context doesn't cover the question, you may answer using your own general football knowledge instead — but only if the question is about La Liga, Premier League, or Champions League.
Conversation so far:
If you're not confident in the answer either way, say so honestly rather than guessing.
Use the conversation history to understand follow-up questions (e.g. "why not X" refers to the previous topic).""
{history_text}

Context:
{context_text}

Question: {query}"""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return "Sorry, I'm having trouble reaching the football brain right now — please try again in a moment."

if __name__ == "__main__":
    chat_history = []
    while True:
        user_input = input("\nAsk Egosa: ")
        if user_input.lower() in ["quit", "exit"]:
            break

        answer = ask_egosa(user_input, chat_history)
        print(answer)

        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": answer})