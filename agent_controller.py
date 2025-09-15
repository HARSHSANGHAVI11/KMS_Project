from agents.doc_expert import answer_with_doc_expert
from agents.summary_bot import summarize_with_bot

def decide_agent(prompt: str):
    if "summary" in prompt.lower() or "summarize" in prompt.lower():
        return summarize_with_bot(prompt)  # → uses Mistral
    else:
        return answer_with_doc_expert(prompt)  # → uses LLaMA3

