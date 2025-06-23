import os
import faiss
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 1. Load documents
def load_documents(folder):
    docs = []
    for fname in os.listdir(folder):
        path = os.path.join(folder, fname)
        if os.path.isfile(path) and fname.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                docs.append(f.read())
    return docs

# 2. Chunk text
def chunk_text(text, chunk_size=300):
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

# 3. Embed chunks
def embed_chunks(chunks, model):
    return model.encode(chunks, convert_to_numpy=True)

# 4. Build FAISS index
def build_index(vectors):
    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)
    return index

# 5. Retrieve top-k chunks
def retrieve(query, model, index, chunks, k=3):
    query_vector = model.encode([query])
    distances, indices = index.search(query_vector, k)
    return [chunks[i] for i in indices[0]]

# 6. Use Gemini to generate answer
def generate_answer(query, context_chunks, chat_history):
    context = "\n\n".join(context_chunks)

    history_block = ""
    for turn in chat_history[-5:]:  # limit to last 5 turns
        history_block += f"User: {turn['user']}\nBot: {turn['bot']}\n"

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

# --- MAIN APP ---
if __name__ == "__main__":
    print("Loading documents from ./docs/ ...")
    documents = load_documents("docs/")
    
    print("Splitting and chunking ...")
    chunks = []
    for doc in documents:
        chunks.extend(chunk_text(doc))

    print("Embedding chunks ...")
    embed_model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = embed_chunks(chunks, embed_model)

    print("Building FAISS index ...")
    index = build_index(embeddings)

    chat_history = []
    print("Ready. Ask questions or type 'exit' to quit.")
    while True:
        query = input("\n> ")
        if query.strip().lower() in ["exit", "quit"]:
            break

        top_chunks = retrieve(query, embed_model, index, chunks)
        answer = generate_answer(query, top_chunks, chat_history)

        # Save to history
        chat_history.append({"user": query, "bot": answer})
        print("\nHistory:\n", chat_history)
        print("\nAnswer:\n", answer)