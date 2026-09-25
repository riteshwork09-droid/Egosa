import os
from dotenv import load_dotenv
from google import genai
from retriever import retrieve

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

ALLOWED_KEYWORDS = [
    "la liga",
    "laliga",
    "premier league",
    "epl",
    "champions league",
    "ucl",
    "football",
    "soccer"
]


def is_on_topic(query):
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in ALLOWED_KEYWORDS)


def ask_egosa(query):
    if not is_on_topic(query):
        return "I'm Egosa — I only answer questions about La Liga, Premier League, and Champions League football."

    context = retrieve(query)
    context_text = "\n".join(context)

    prompt = f"""You are Egosa, a football chatbot for La Liga, Premier League, and Champions League only.

Use ONLY the context below to answer.
If the context doesn't cover the question, say you don't have that information.

Context:
{context_text}

Question: {query}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text


if __name__ == "__main__":
    while True:
        user_input = input("\nAsk Egosa: ")

        if user_input.lower() in ["quit", "exit"]:
            break

        print(ask_egosa(user_input))