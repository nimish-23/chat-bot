from flask import Blueprint, request, jsonify, render_template, Response
import time
from app.core.logger import logger

chat_bp = Blueprint('chat', __name__)

# Serve frontend
@chat_bp.route('/')
def index():
    return render_template('index.html')

chat_service = None

def init_routes(service):
    global chat_service
    chat_service = service

@chat_bp.route('/chat', methods=['POST'])
def chat():
    
    try:
        data = request.get_json()
        
        if data is None:
            return jsonify({'error': 'Invalid JSON'}), 400
        
        messages = data.get('messages', [])
        temperature = data.get('temperature', 0.7)
        
        response = chat_service.chat(messages, temperature=temperature)
        
        return jsonify(response), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
        
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@chat_bp.route('/chat/stream', methods=['POST'])
def stream_chat():
    """Streaming chat endpoint - returns Server-Sent Events (SSE)"""
    try:
        data = request.get_json()
        
        if data is None:
            return jsonify({'error': 'Invalid JSON'}), 400
        
        messages = data.get('messages', [])
        temperature = data.get('temperature', 0.7)
        
        def generate():
            """Generator function for streaming response with timing"""
            start_time = time.time()
            chunk_count = 0
            
            try:
                for chunk in chat_service.stream_chat(messages, temperature=temperature):
                    chunk_count += 1
                    # Send each chunk as Server-Sent Event
                    yield f"data: {chunk}\n\n"
                
                # Log after streaming completes
                end_time = time.time()
                latency = end_time - start_time
                logger.info(
                    f"Streaming completed | "
                    f"Model: {chat_service.llm.model} | "
                    f"Latency: {latency:.3f}s | "
                    f"Chunks: {chunk_count}"
                )
                
            except Exception as e:
                logger.error(f"Streaming error: {str(e)}")
                yield f"data: [ERROR: {str(e)}]\n\n"
        
        return Response(generate(), mimetype='text/event-stream')
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
        
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500