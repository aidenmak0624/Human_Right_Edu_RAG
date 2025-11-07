from flask import Blueprint, jsonify

bp = Blueprint('health', __name__)

@bp.route('/api/health', methods=['GET'])
def health_check():
    """
    Check if API is running
    
    Returns:
        {
            "status": "healthy",
            "message": "Human Rights RAG API is running"
        }
    """
    return jsonify({
        'status': 'healthy',
        'message': 'Human Rights RAG API is running'
    }), 200