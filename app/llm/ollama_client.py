import requests
from app.llm.base import BaseLLM

class OllamaLLM(BaseLLM):

    def __init__(self, model="llama3.2", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url

    def generate(self, messages: list, temperature: float = 0.7):

        url = f"{self.base_url}/api/chat"

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": False
        }

        try:
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()

            data = response.json()

            return {
                "content": data["message"]["content"],
                "model": self.model,
                "usage": data.get("usage", {})
            }

        except requests.exceptions.RequestException as e:
            raise Exception(f"Ollama API error: {str(e)}")
