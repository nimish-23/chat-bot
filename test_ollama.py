from app.llm.ollama_client import OllamaLLM

# Test the OllamaLLM client
llm = OllamaLLM(model="llama3.2")

messages = [
    {"role": "user", "content": "Say hello in one sentence"}
]

print("Testing OllamaLLM client...")
try:
    response = llm.generate(messages)
    print("\n✓ Success!")
    print(f"Model: {response['model']}")
    print(f"Response: {response['content']}")
    if response.get('usage'):
        print(f"Usage: {response['usage']}")
except Exception as e:
    print(f"\n✗ Error: {e}")
