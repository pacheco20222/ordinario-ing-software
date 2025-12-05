from datetime import datetime
from bson import ObjectId
from app import db


class Match:
    """Match model for MongoDB operations"""
    
    COLLECTION_NAME = 'matches'
    
    @staticmethod
    def get_collection():
        """Get the matches collection"""
        if db is None:
            raise ConnectionError("MongoDB connection not available. Please check your MONGODB_URI.")
        return db[Match.COLLECTION_NAME]
    
    @staticmethod
    def create(user_id_1, user_id_2):
        """
        Create a new match between two users
        Stores user IDs in sorted order to avoid duplicates
        Args:
            user_id_1: First user ID (ObjectId or string)
            user_id_2: Second user ID (ObjectId or string)
        Returns:
            Inserted match document with _id
        """
        collection = Match.get_collection()
        if isinstance(user_id_1, str):
            user_id_1 = ObjectId(user_id_1)
        if isinstance(user_id_2, str):
            user_id_2 = ObjectId(user_id_2)
        
        # Sort user IDs to ensure consistent storage (avoid duplicates)
        sorted_ids = sorted([user_id_1, user_id_2])
        
        match_data = {
            'user_id_1': sorted_ids[0],
            'user_id_2': sorted_ids[1],
            'created_at': datetime.utcnow()
        }
        
        # Check if match already exists
        existing = collection.find_one({
            'user_id_1': sorted_ids[0],
            'user_id_2': sorted_ids[1]
        })
        
        if existing:
            return existing
        
        result = collection.insert_one(match_data)
        match_data['_id'] = result.inserted_id
        return match_data
    
    @staticmethod
    def find_by_users(user_id_1, user_id_2):
        """
        Find match between two users
        Args:
            user_id_1: First user ID (ObjectId or string)
            user_id_2: Second user ID (ObjectId or string)
        Returns:
            Match document or None
        """
        collection = Match.get_collection()
        if isinstance(user_id_1, str):
            user_id_1 = ObjectId(user_id_1)
        if isinstance(user_id_2, str):
            user_id_2 = ObjectId(user_id_2)
        
        # Sort user IDs for consistent lookup
        sorted_ids = sorted([user_id_1, user_id_2])
        
        return collection.find_one({
            'user_id_1': sorted_ids[0],
            'user_id_2': sorted_ids[1]
        })
    
    @staticmethod
    def find_all_by_user(user_id):
        """
        Find all matches for a user
        Args:
            user_id: User ID (ObjectId or string)
        Returns:
            List of match documents
        """
        collection = Match.get_collection()
        if isinstance(user_id, str):
            user_id = ObjectId(user_id)
        
        # Find all matches where user is either user_id_1 or user_id_2
        matches = collection.find({
            '$or': [
                {'user_id_1': user_id},
                {'user_id_2': user_id}
            ]
        }).sort('created_at', -1)  # Sort by most recent first
        
        return list(matches)
    
    @staticmethod
    def to_dict(match_doc):
        """
        Convert match document to dictionary
        Args:
            match_doc: MongoDB match document
        Returns:
            dict representation
        """
        if not match_doc:
            return None
        
        match_dict = {
            '_id': str(match_doc['_id']),
            'user_id_1': str(match_doc['user_id_1']),
            'user_id_2': str(match_doc['user_id_2']),
            'created_at': match_doc.get('created_at').isoformat() if match_doc.get('created_at') else None
        }
        return match_dict

