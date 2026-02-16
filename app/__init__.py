from flask import Flask
from flask_cors import CORS
from app.llm.ollama_client import OllamaLLM
from app.services.chat_service import ChatService
from app.api.chat_routes import chat_bp, init_routes

def create_app():
    
    app = Flask(__name__)
    
    # Enable CORS for frontend
    CORS(app)
    
    llm = OllamaLLM()
    chat_service = ChatService(llm)
    
    init_routes(chat_service)
    
    app.register_blueprint(chat_bp)
    
    return app