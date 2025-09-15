from models.llm_loader import query_model

def summarize_with_bot(prompt: str):
    return query_model(f"Summarize clearly:\n{prompt}", model="mistral")
