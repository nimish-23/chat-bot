from flask import Blueprint, request, jsonify

chat_bp = Blueprint('chat', __name__)

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