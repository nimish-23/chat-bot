from flask import Blueprint, request, jsonify, render_template

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
            """Generator function for streaming response"""
            try:
                for chunk in chat_service.stream_chat(messages, temperature=temperature):
                    # Send each chunk as Server-Sent Event
                    yield f"data: {chunk}\n\n"
            except Exception as e:
                yield f"data: [ERROR: {str(e)}]\n\n"
        
        from flask import Response
        return Response(generate(), mimetype='text/event-stream')
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
        
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500