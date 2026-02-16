class ChatService:

    def __init__(self, llm):
        self.llm = llm

    def chat(self, messages: list, **kwargs):
       
        if not messages:
            raise ValueError("Messages cannot be empty")
        
        if not isinstance(messages, list):
            raise ValueError("Messages must be a list")
        
        for msg in messages:
            if not isinstance(msg, dict):
                raise ValueError("Each message must be a dictionary")
            if 'role' not in msg or 'content' not in msg:
                raise ValueError("Each message must have 'role' and 'content' keys")
        
        try:
            response = self.llm.generate(messages, **kwargs)
            return response
        except Exception as e:
            raise Exception(f"Failed to generate response: {str(e)}")

    def stream_chat(self, messages: list, **kwargs):
        if not messages:
            raise ValueError("Messages cannot be empty")
        
        if not isinstance(messages, list):
            raise ValueError("Messages must be a list")
        
        for msg in messages:
            if not isinstance(msg, dict):
                raise ValueError("Each message must be a dictionary")
            if 'role' not in msg or 'content' not in msg:
                raise ValueError("Each message must have 'role' and 'content' keys")
        
        try:
            response = self.llm.stream_generate(messages, **kwargs)
            return response
        except Exception as e:
            raise Exception(f"Failed to generate response: {str(e)}")   