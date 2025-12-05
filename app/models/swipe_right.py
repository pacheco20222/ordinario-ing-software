from datetime import datetime
from bson import ObjectId
from app import db


class SwipeRight:
    """SwipeRight model for MongoDB operations"""
    
    COLLECTION_NAME = 'swipe_right'
    
    @staticmethod
    def get_collection():
        """Get the swipe_right collection"""
        if db is None:
            raise ConnectionError("MongoDB connection not available. Please check your MONGODB_URI.")
        return db[SwipeRight.COLLECTION_NAME]
    
    @staticmethod
    def create(user_id, swiped_user_id):
        """
        Create a new swipe right relationship
        Args:
            user_id: User who made the swipe (ObjectId or string)
            swiped_user_id: User who was swiped right (ObjectId or string)
        Returns:
            Inserted swipe_right document with _id
        """
        collection = SwipeRight.get_collection()
        if isinstance(user_id, str):
            user_id = ObjectId(user_id)
        if isinstance(swiped_user_id, str):
            swiped_user_id = ObjectId(swiped_user_id)
        
        swipe_data = {
            'user_id': user_id,
            'swiped_user_id': swiped_user_id,
            'created_at': datetime.utcnow()
        }
        
        # Check if swipe already exists to avoid duplicates
        existing = collection.find_one({
            'user_id': user_id,
            'swiped_user_id': swiped_user_id
        })
        
        if existing:
            return existing
        
        result = collection.insert_one(swipe_data)
        swipe_data['_id'] = result.inserted_id
        return swipe_data
    
    @staticmethod
    def find_by_users(user_id, swiped_user_id):
        """
        Find swipe right relationship between two users
        Args:
            user_id: User ID (ObjectId or string)
            swiped_user_id: Swiped user ID (ObjectId or string)
        Returns:
            SwipeRight document or None
        """
        collection = SwipeRight.get_collection()
        if isinstance(user_id, str):
            user_id = ObjectId(user_id)
        if isinstance(swiped_user_id, str):
            swiped_user_id = ObjectId(swiped_user_id)
        
        return collection.find_one({
            'user_id': user_id,
            'swiped_user_id': swiped_user_id
        })
    
    @staticmethod
    def delete_by_users(user_id, swiped_user_id):
        """
        Delete swipe right relationship between two users
        Args:
            user_id: User ID (ObjectId or string)
            swiped_user_id: Swiped user ID (ObjectId or string)
        Returns:
            True if deleted, False if not found
        """
        collection = SwipeRight.get_collection()
        if isinstance(user_id, str):
            user_id = ObjectId(user_id)
        if isinstance(swiped_user_id, str):
            swiped_user_id = ObjectId(swiped_user_id)
        
        result = collection.delete_one({
            'user_id': user_id,
            'swiped_user_id': swiped_user_id
        })
        
        return result.deleted_count > 0
    
    @staticmethod
    def to_dict(swipe_doc):
        """
        Convert swipe_right document to dictionary
        Args:
            swipe_doc: MongoDB swipe_right document
        Returns:
            dict representation
        """
        if not swipe_doc:
            return None
        
        swipe_dict = {
            '_id': str(swipe_doc['_id']),
            'user_id': str(swipe_doc['user_id']),
            'swiped_user_id': str(swipe_doc['swiped_user_id']),
            'created_at': swipe_doc.get('created_at').isoformat() if swipe_doc.get('created_at') else None
        }
        return swipe_dict

