import time
from app.core.logger import logger
from app.llm.ollama_client import OllamaLLM


class ChatService:

    def __init__(self, llm):
        self.llm = llm
        self.total_requests = 0
        self.total_latency = 0.0  
        self.model_name = llm.model

    def chat(self, messages: list, **kwargs):

        start_time = time.time()
       
        if not messages:
            logger.error("Messages cannot be empty")
            raise ValueError("Messages cannot be empty")
        
        if not isinstance(messages, list):
            logger.error("Messages must be a list")
            raise ValueError("Messages must be a list")
        
        for msg in messages:
            if not isinstance(msg, dict):
                logger.error("Each message must be a dictionary")
                raise ValueError("Each message must be a dictionary")
            if 'role' not in msg or 'content' not in msg:
                logger.error("Each message must have 'role' and 'content' keys")
                raise ValueError("Each message must have 'role' and 'content' keys")
        
        try:
            return self.llm.generate(messages, **kwargs)
               
        except Exception as e:
            logger.exception("Error generating response")
            raise Exception(f"Error generating response: {str(e)}")

    def stream_chat(self, messages: list, **kwargs):

        if not messages:
            logger.error("Messages cannot be empty")
            raise ValueError("Messages cannot be empty")
        
        if not isinstance(messages, list):
            logger.error("Messages must be a list")
            raise ValueError("Messages must be a list")
        
        for msg in messages:
            if not isinstance(msg, dict):
                logger.error("Each message must be a dictionary")
                raise ValueError("Each message must be a dictionary")
            if 'role' not in msg or 'content' not in msg:
                logger.error("Each message must have 'role' and 'content' keys")
                raise ValueError("Each message must have 'role' and 'content' keys")
        
        try:
            # Return the generator - timing is handled in the route layer
            return self.llm.stream_generate(messages, **kwargs)
            
        except Exception as e:
            logger.exception("Error generating streaming response")
            raise Exception(f"Error generating streaming response: {str(e)}")     