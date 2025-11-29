import os
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration"""
    
    # MongoDB Configuration
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/music_dating')
    # Extract database name from URI if not explicitly set
    _db_name_from_env = os.getenv('MONGODB_DB_NAME')
    if _db_name_from_env:
        MONGODB_DB_NAME = _db_name_from_env
    else:
        # Try to extract from URI
        try:
            parsed = urlparse(MONGODB_URI)
            if parsed.path and parsed.path != '/':
                MONGODB_DB_NAME = parsed.path.strip('/').split('/')[0]
            else:
                MONGODB_DB_NAME = 'music_dating_db'
        except:
            MONGODB_DB_NAME = 'music_dating_db'
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default-secret-key-change-in-production')
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRATION_HOURS = 24
    
    # Flask Configuration
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'default-flask-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    PORT = int(os.getenv('PORT', 5001))

