class BaseLLM:
    def generate(self, messages: list, **kwargs):
        raise NotImplementedError("Subclasses must implement generate()")
