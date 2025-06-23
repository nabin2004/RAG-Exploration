import os
import faiss
import requests
from dotenv import load_dotenv
import numpy as np
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

API_BASE = "http://localhost:8000/api/core/"
CHUNKS_URL = f"{API_BASE}chunks/"
EMBEDDINGS_URL = f"{API_BASE}embeddings/"
CHAT_MESSAGES_URL = f"{API_BASE}chatmessages/"
SESSION_ID = 1  # Static for now

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def load_chunks_and_embeddings():
    try:
        chunk_res = requests.get(CHUNKS_URL)
        embed_res = requests.get(EMBEDDINGS_URL)

        chunk_res.raise_for_status()
        embed_res.raise_for_status()

        chunks = chunk_res.json()
        embeddings = embed_res.json()

        # Map chunk ID to content
        chunk_id_to_content = {chunk["id"]: chunk["content"] for chunk in chunks}
        vectors = []
        ordered_chunks = []

        for emb in embeddings:
            chunk_id = emb["chunk"]
            vector = emb["vector"]
            if chunk_id in chunk_id_to_content:
                ordered_chunks.append(chunk_id_to_content[chunk_id])
                vectors.append(vector)

        print(f"Loaded {len(vectors)} embeddings and chunks from DB.")
        return ordered_chunks, np.array(vectors).astype("float32")

    except Exception as e:
        print("Error loading chunks/embeddings:", e)
        return [], np.array([])

def build_index(vectors):
    if len(vectors) == 0:
        print("No vectors to index.")
        return None
    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)
    return index

def retrieve(query, model, index, chunks, k=3):
    query_vector = model.encode([query]).astype("float32")
    distances, indices = index.search(query_vector, k)
    return [chunks[i] for i in indices[0]]

def get_chat_history(session_id):
    try:
        res = requests.get(CHAT_MESSAGES_URL, params={"session": session_id})
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print("Error fetching history:", e)
        return []

def post_message(role, content, session_id):
    try:
        res = requests.post(CHAT_MESSAGES_URL, json={
            "role": role,
            "content": content,
            "session": session_id
        })
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"Error posting {role} message:", e)
        return None    print("Fetching chunks and embeddings from backend ...")
    chunks, vectors = load_chunks_and_embeddings()

    if not chunks or vectors.size == 0:
        print("No data available for search.")
        return

    index = build_index(vectors)
    chat_loop(embed_model, index, chunks)

if __name__ == "__main__":
    main()


def generate_answer(query, context_chunks, chat_history):
    context = "\n\n".join(context_chunks)
    history_block = "\n".join(
        f"{msg['role'].capigenerate_answertalize()}: {msg['content']}"
        for msg in chat_history[-10:]
    )

    prompt = f"""You are a helpful assistant. Use the provided context and past conversation to answer.

Context:
{context}

Conversation History:
{history_block}

User: {query}
Bot:"""

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

def chat_loop(model, index, chunks):
    chat_history = get_chat_history(SESSION_ID)

    print("\nReady to chat. Commands: 'history', 'clear', 'quit'.")
    while True:
        query = input("\n> ").strip()
        if query in {"quit", "exit"}:
            print("Goodbye.")
            break
        if query == "history":
            for i, turn in enumerate(chat_history):
                print(f"{i+1}. {turn['role'].capitalize()}: {turn['content']}")
            continue
        if query == "clear":
            print("Clear functionality not implemented yet.")
            continue

        post_message("user", query, SESSION_ID)

        top_chunks = retrieve(query, model, index, chunks)
        answer = generate_answer(query, top_chunks, chat_history)

        post_message("bot", answer, SESSION_ID)
        chat_history.append({"role": "user", "content": query})
        chat_history.append({"role": "bot", "content": answer})

        print("\nBot:\n", answer)

def main():
    print("Fetching chunks and embeddings from backend ...")
    chunks, vectors = load_chunks_and_embeddings()

    if not chunks or vectors.size == 0:
        print("No data available for search.")
        return

    index = build_index(vectors)
    chat_loop(embed_model, index, chunks)

if __name__ == "__main__":
    main()
