from datetime import datetime
from bson import ObjectId
from app import db


class User:
    """User model for MongoDB operations"""
    
    COLLECTION_NAME = 'users'
    
    @staticmethod
    def get_collection():
        """Get the users collection"""
        if db is None:
            raise ConnectionError("MongoDB connection not available. Please check your MONGODB_URI.")
        return db[User.COLLECTION_NAME]
    
    @staticmethod
    def create(user_data):
        """
        Create a new user
        Args:
            user_data: dict with email, password (hashed), favorite_songs, favorite_artists, favorite_genres, spotify_username
        Returns:
            Inserted user document with _id
        """
        collection = User.get_collection()
        user_data['created_at'] = datetime.utcnow()
        user_data['updated_at'] = datetime.utcnow()
        result = collection.insert_one(user_data)
        user_data['_id'] = result.inserted_id
        return user_data
    
    @staticmethod
    def find_by_email(email):
        """
        Find user by email
        Args:
            email: User email
        Returns:
            User document or None
        """
        collection = User.get_collection()
        return collection.find_one({'email': email})
    
    @staticmethod
    def find_by_id(user_id):
        """
        Find user by ID
        Args:
            user_id: User ObjectId or string
        Returns:
            User document or None
        """
        collection = User.get_collection()
        if isinstance(user_id, str):
            user_id = ObjectId(user_id)
        return collection.find_one({'_id': user_id})
    
    @staticmethod
    def update(user_id, update_data):
        """
        Update user data
        Args:
            user_id: User ObjectId or string
            update_data: dict with fields to update
        Returns:
            Updated user document or None
        """
        collection = User.get_collection()
        if isinstance(user_id, str):
            user_id = ObjectId(user_id)
        
        update_data['updated_at'] = datetime.utcnow()
        result = collection.find_one_and_update(
            {'_id': user_id},
            {'$set': update_data},
            return_document=True
        )
        return result
    
    @staticmethod
    def to_dict(user_doc):
        """
        Convert user document to dictionary, excluding password
        Args:
            user_doc: MongoDB user document
        Returns:
            dict without password field
        """
        if not user_doc:
            return None
        
        user_dict = {
            '_id': str(user_doc['_id']),
            'email': user_doc.get('email'),
            'favorite_songs': user_doc.get('favorite_songs', []),
            'favorite_artists': user_doc.get('favorite_artists', []),
            'favorite_genres': user_doc.get('favorite_genres', []),
            'spotify_username': user_doc.get('spotify_username'),
            'created_at': user_doc.get('created_at').isoformat() if user_doc.get('created_at') else None,
            'updated_at': user_doc.get('updated_at').isoformat() if user_doc.get('updated_at') else None
        }
        return user_dict

