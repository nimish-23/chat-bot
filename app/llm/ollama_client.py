import requests
import json
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

    def stream_generate(self, messages: list, temperature: float = 0.7):

        url = f"{self.base_url}/api/chat"

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": True
        }

        try:
            response = requests.post(url, json=payload, timeout=60, stream=True)
            response.raise_for_status()

            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    if "message" in data and "content" in data["message"]:
                        yield data["message"]["content"]

        except requests.exceptions.RequestException as e:
            raise Exception(f"Ollama API error: {str(e)}")  