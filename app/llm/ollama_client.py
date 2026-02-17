import requests
import json
import time
from app.llm.base import BaseLLM
from app.core.logger import logger  

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
            start_time = time.time()

            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()

            end_time = time.time()
            latency = end_time - start_time

            logger.info(
                f"Model: {self.model} | "
                f"Latency: {latency:.3f}s | "
                f"Requests: 1"
            )
            data = response.json()

            return {
                "content": data["message"]["content"],
                "model": self.model,
                "usage": data.get("usage", {})
            }

        except requests.exceptions.RequestException as e:
            logger.exception("Ollama API error")
            raise 

    def stream_generate(self, messages: list, temperature: float = 0.7):

        url = f"{self.base_url}/api/chat"

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": True
        }

        try:
            start_time = time.time()

            response = requests.post(url, json=payload, timeout=60, stream=True)
            response.raise_for_status()

            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    if "message" in data and "content" in data["message"]:
                        yield data["message"]["content"]

            end_time = time.time()
            latency = end_time - start_time

            logger.info(
                f"Model: {self.model} | "
                f"Latency: {latency:.3f}s | "
                f"Requests: 1"
            )

        except requests.exceptions.RequestException as e:
            logger.exception("Ollama API error")
            raise  