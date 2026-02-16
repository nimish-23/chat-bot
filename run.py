from flask import Flask, request, jsonify
from app.llm.ollama_client import OllamaLLM

app = Flask(__name__)
llm = OllamaLLM()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    response = llm.generate(data['messages'])
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
