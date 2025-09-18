import requests

def query_model(prompt: str, model: str = "mistral") -> str:
    """
    Sends prompt to Ollama via REST API using the specified model.
    """
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        return f"Error querying model '{model}': {str(e)}"
