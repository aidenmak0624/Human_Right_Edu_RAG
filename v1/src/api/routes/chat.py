
from flask import Blueprint, request, jsonify
from src.core.rag_system import SimpleRAG
import logging

bp = Blueprint('chat', __name__)

# Initialize RAG system (singleton)
rag_system = None

def get_rag_system():
    """Get or create RAG system instance"""
    global rag_system
    if rag_system is None:
        rag_system = SimpleRAG(preload_topics=True)
    return rag_system


@bp.route('/api/chat', methods=['POST'])
def chat():
    """
    Process a chat query
    
    Request JSON:
    {
        "query": "What are human rights?",
        "topic": "foundational_rights",
        "difficulty": "intermediate"  # optional
    }
    
    Response JSON:
    {
        "answer": "Human rights are...",
        "sources": ["udhr.txt", "bill_of_rights.txt"],
        "topic": "foundational_rights"
    }
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate required fields
        query = data.get('query')
        topic = data.get('topic')
        difficulty = data.get('difficulty', 'intermediate')
        
        if not query:
            return jsonify({'error': 'Missing required field: query'}), 400
        
        if not topic:
            return jsonify({'error': 'Missing required field: topic'}), 400
        
        # Validate topic
        valid_topics = [
            'foundational_rights',
            'childrens_rights',
            'womens_rights',
            'indigenous_rights',
            'minority_rights',
            'civil_political_rights',
            'freedom_expression',
            'economic_social_cultural',
            'right_to_education'
        ]
        
        if topic not in valid_topics:
            return jsonify({'error': f'Invalid topic. Must be one of: {", ".join(valid_topics)}'}), 400
        
        # Get RAG system
        rag = get_rag_system()
        
        # Generate answer
        answer = rag.generate_answer(query, topic, difficulty)
        
        # Extract sources from answer (they're in the format "📚 Sources: file1.txt, file2.txt")
        sources = []
        if "📚 Sources:" in answer:
            parts = answer.split("📚 Sources:")
            answer_text = parts[0].strip()
            sources_text = parts[1].strip()
            sources = [s.strip() for s in sources_text.split(',')]
        else:
            answer_text = answer
        
        # Return response
        return jsonify({
            'answer': answer_text,
            'sources': sources,
            'topic': topic,
            'query': query
        }), 200
        
    except Exception as e:
        logging.error(f"Error in chat endpoint: {e}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@bp.route('/api/topics', methods=['GET'])
def get_topics():
    """
    Get list of available topics
    
    Response JSON:
    {
        "topics": [
            {
                "id": "foundational_rights",
                "name": "Foundational Human Rights",
                "description": "...",
                "document_count": 6
            },
            ...
        ]
    }
    """
    topics = [
        {
            'id': 'foundational_rights',
            'name': 'Foundational Human Rights',
            'description': 'UDHR, Bill of Rights, Vienna Declaration',
            'icon': '📜'
        },
        {
            'id': 'childrens_rights',
            'name': "Children's Rights",
            'description': 'Convention on the Rights of the Child',
            'icon': '👶'
        },
        {
            'id': 'womens_rights',
            'name': "Women's Rights",
            'description': 'CEDAW and gender equality',
            'icon': '👩'
        },
        {
            'id': 'indigenous_rights',
            'name': 'Indigenous Peoples\' Rights',
            'description': 'UNDRIP and ILO 169',
            'icon': '🌏'
        },
        {
            'id': 'minority_rights',
            'name': 'Minority Rights',
            'description': 'Protection and anti-discrimination',
            'icon': '🤝'
        },
        {
            'id': 'civil_political_rights',
            'name': 'Civil & Political Rights',
            'description': 'ICCPR and fundamental freedoms',
            'icon': '⚖️'
        },
        {
            'id': 'freedom_expression',
            'name': 'Freedom of Expression',
            'description': 'Speech and assembly rights',
            'icon': '💬'
        },
        {
            'id': 'economic_social_cultural',
            'name': 'Economic, Social & Cultural Rights',
            'description': 'ICESCR standards',
            'icon': '💼'
        },
        {
            'id': 'right_to_education',
            'name': 'Right to Education',
            'description': 'Educational rights and access',
            'icon': '📚'
        }
    ]
    
    return jsonify({'topics': topics}), 200