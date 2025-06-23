1. RAG
2. remember prior conversation turns

# RAG Components:
1. Load documents
2. Chunk texts
3. Embed Chunks
4. Build FAISS (Facebook AI Similarity Search) index
5. Retrieve top-k chunks
6. I am using Gemini to generate answer
7. Saves the chat history and uses for statefullness

- Save history on normal list

```
python rag.py
```