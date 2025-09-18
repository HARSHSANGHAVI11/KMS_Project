import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""  # ✅ Force CPU
import pickle
import faiss
import torch
# ✅ Prevent GPU `.to()` issues when forcing CPU
def _noop_to(self, *args, **kwargs):
    return self
torch.nn.Module.to = _noop_to

from sentence_transformers import SentenceTransformer
from app.agent_controller import decide_agent

INDEX_DIR = "data/index"

# ✅ Load offline embedding model (CPU)
local_model_path = r"C:\models\all-MiniLM-L6-v2"
embedding_model = SentenceTransformer(local_model_path)
embedding_model._target_device = 'cpu'

# ✅ Memory: Keep last few conversation messages
chat_history = []  # [(user_msg, agent_msg), ...]

def get_answer(query: str, doc_name: str):
    """
    Retrieve the most relevant document data + updates + code,
    combine with recent chat history, and generate an AI answer.
    """
    index_path = os.path.join(INDEX_DIR, f"{doc_name}.index")
    chunks_path = os.path.join(INDEX_DIR, f"{doc_name}_chunks.pkl")

    if not os.path.exists(index_path) or not os.path.exists(chunks_path):
        return f"Document '{doc_name}' not found."

    # ✅ Load FAISS index and document chunks
    index = faiss.read_index(index_path)
    with open(chunks_path, "rb") as f:
        chunks = pickle.load(f)

    # ✅ Vector search for top 10 most relevant chunks (old document)
    q_embed = embedding_model.encode([query])
    D, I = index.search(q_embed, k=10)
    retrieved_chunks = [chunks[i] for i in I[0]]

    # ✅ Collect updates (chunks that start with "[")
    update_chunks = [c for c in chunks if isinstance(c, str) and c.startswith("[")]

    # ✅ Collect all code snippets first
    code_chunks = [c for c in chunks if "[CODE]" in c]

    # ✅ Build context: Code → Old Data → Updates
    context = "\n\n".join(code_chunks + retrieved_chunks + update_chunks)

    # ✅ Limit very large context to ~20k chars
    max_chars = 20000
    if len(context) > max_chars:
        context = context[:max_chars] + "\n...[Context Truncated]..."

    # ✅ Include recent chat history (last 3 exchanges)
    history_text = "\n".join([f"User: {u}\nAgent: {a}" for u, a in chat_history[-3:]])

    # ✅ Build final prompt
    prompt = f"""You are an AI assistant answering based on the original document, updates, and prior conversation.
If the user requests code, include the exact snippet first. 
Otherwise, provide logic/explanation with both old and updated details.


Context from document and updates:
{context}

User Question:
{query}

Answer:"""

    # ✅ Decide which agent answers
    answer = decide_agent(prompt)

    # ✅ Save to chat memory
    chat_history.append((query, answer))

    return answer

def clear_memory():
    """Reset chat history."""
    chat_history.clear()
