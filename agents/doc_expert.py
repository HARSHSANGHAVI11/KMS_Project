from models.llm_loader import query_model

def answer_with_doc_expert(prompt: str):
    return query_model(prompt, model="llama3")
