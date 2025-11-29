from datetime import datetime
from bson import ObjectId
from app import db


class Playlist:
    """Playlist model for MongoDB operations"""
    
    COLLECTION_NAME = 'playlists'
    
    @staticmethod
    def get_collection():
        """Get the playlists collection"""
        if db is None:
            raise ConnectionError("MongoDB connection not available. Please check your MONGODB_URI.")
        return db[Playlist.COLLECTION_NAME]
    
    @staticmethod
    def create(playlist_data):
        """
        Create a new playlist
        Args:
            playlist_data: dict with user_id and songs array
        Returns:
            Inserted playlist document with _id
        """
        collection = Playlist.get_collection()
        if isinstance(playlist_data['user_id'], str):
            playlist_data['user_id'] = ObjectId(playlist_data['user_id'])
        
        playlist_data['created_at'] = datetime.utcnow()
        playlist_data['updated_at'] = datetime.utcnow()
        result = collection.insert_one(playlist_data)
        playlist_data['_id'] = result.inserted_id
        return playlist_data
    
    @staticmethod
    def find_by_user_id(user_id):
        """
        Find playlist by user ID
        Args:
            user_id: User ObjectId or string
        Returns:
            Playlist document or None
        """
        collection = Playlist.get_collection()
        if isinstance(user_id, str):
            user_id = ObjectId(user_id)
        return collection.find_one({'user_id': user_id})
    
    @staticmethod
    def update_or_create(user_id, songs):
        """
        Update existing playlist or create new one
        Args:
            user_id: User ObjectId or string
            songs: Array of song objects with song_name and artist_name
        Returns:
            Playlist document
        """
        collection = Playlist.get_collection()
        if isinstance(user_id, str):
            user_id = ObjectId(user_id)
        
        playlist_data = {
            'user_id': user_id,
            'songs': songs,
            'updated_at': datetime.utcnow()
        }
        
        existing = collection.find_one({'user_id': user_id})
        
        if existing:
            # Update existing playlist
            result = collection.find_one_and_update(
                {'user_id': user_id},
                {'$set': playlist_data},
                return_document=True
            )
            return result
        else:
            # Create new playlist
            playlist_data['created_at'] = datetime.utcnow()
            result = collection.insert_one(playlist_data)
            playlist_data['_id'] = result.inserted_id
            return playlist_data
    
    @staticmethod
    def to_dict(playlist_doc):
        """
        Convert playlist document to dictionary
        Args:
            playlist_doc: MongoDB playlist document
        Returns:
            dict representation
        """
        if not playlist_doc:
            return None
        
        playlist_dict = {
            '_id': str(playlist_doc['_id']),
            'user_id': str(playlist_doc['user_id']),
            'songs': playlist_doc.get('songs', []),
            'created_at': playlist_doc.get('created_at').isoformat() if playlist_doc.get('created_at') else None,
            'updated_at': playlist_doc.get('updated_at').isoformat() if playlist_doc.get('updated_at') else None
        }
        return playlist_dict

