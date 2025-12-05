from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from app.config import Config

# Initialize MongoDB client
mongo_client = None
db = None


def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY
    
    # Enable CORS
    CORS(app)
    
    # Initialize MongoDB connection with timeout and error handling
    global mongo_client, db
    try:
        # Set connection timeout to avoid blocking workers
        mongo_client = MongoClient(
            Config.MONGODB_URI,
            serverSelectionTimeoutMS=5000,  # 5 second timeout
            connectTimeoutMS=10000,  # 10 second connection timeout
            socketTimeoutMS=20000  # 20 second socket timeout
        )
        # Test the connection
        mongo_client.admin.command('ping')
        db = mongo_client[Config.MONGODB_DB_NAME]
        print(f"✓ Connected to MongoDB: {Config.MONGODB_DB_NAME}")
    except Exception as e:
        print(f"⚠ Warning: MongoDB connection failed: {str(e)}")
        print("⚠ The app will start but database operations will fail until MongoDB is available")
        # Create a dummy client to prevent errors
        mongo_client = None
        db = None
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.profile import profile_bp
    from app.routes.playlist import playlist_bp
    from app.routes.discover import discover_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(profile_bp, url_prefix='/api/profile')
    app.register_blueprint(playlist_bp, url_prefix='/api/playlist')
    app.register_blueprint(discover_bp, url_prefix='/api/discover')
    
    @app.route('/')
    def health_check():
        return {'status': 'ok', 'message': 'Heartbeat Dating App Backend API'}, 200
    
    return app


# Create app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=Config.PORT)

