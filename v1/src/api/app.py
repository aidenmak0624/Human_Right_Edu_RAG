from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    """Create and configure Flask app"""
    # Set template and static folders
    template_dir = os.path.join(os.path.dirname(__file__), '../frontend/templates')
    static_dir = os.path.join(os.path.dirname(__file__), '../frontend/static')
    
    app = Flask(__name__, 
                template_folder=template_dir,
                static_folder=static_dir)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    from src.api.routes import chat, health
    print(f"Health blueprint: {health.bp.name}")
    print(f"Chat blueprint: {chat.bp.name}")
    
    app.register_blueprint(health.bp)
    app.register_blueprint(chat.bp)
    # Frontend route
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/static/<path:filename>')
    def serve_static(filename):
        return send_from_directory(static_dir, filename)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5050, debug=True)
