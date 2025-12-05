from app.models.user import User
from app.models.swipe_right import SwipeRight
from app.models.match import Match


def get_random_user(current_user_id):
    """
    Get a random user profile excluding the current user
    Args:
        current_user_id: Current user ID string
    Returns:
        tuple: (response_dict, status_code)
    """
    # Verify current user exists
    user = User.find_by_id(current_user_id)
    if not user:
        return {'error': 'User not found', 'status_code': 404}, 404
    
    # Get random user
    try:
        random_user = User.find_random_user(current_user_id)
        if not random_user:
            return {'error': 'No other users found', 'status_code': 404}, 404
        
        user_dict = User.to_dict(random_user)
        return user_dict, 200
    except Exception as e:
        return {'error': f'Failed to get random user: {str(e)}', 'status_code': 500}, 500


def swipe_right(current_user_id, swiped_user_id):
    """
    Handle swipe right action and create match if mutual
    Args:
        current_user_id: Current user ID string (user making the swipe)
        swiped_user_id: Swiped user ID string (user being swiped)
    Returns:
        tuple: (response_dict, status_code)
    """
    # Validate users are different
    if current_user_id == swiped_user_id:
        return {'error': 'Cannot swipe right on yourself', 'status_code': 400}, 400
    
    # Verify current user exists
    current_user = User.find_by_id(current_user_id)
    if not current_user:
        return {'error': 'User not found', 'status_code': 404}, 404
    
    # Verify swiped user exists
    swiped_user = User.find_by_id(swiped_user_id)
    if not swiped_user:
        return {'error': 'Swiped user not found', 'status_code': 404}, 404
    
    try:
        # Check if swiped user already swiped right on current user (mutual swipe)
        mutual_swipe = SwipeRight.find_by_users(swiped_user_id, current_user_id)
        
        if mutual_swipe:
            # Both users swiped right - create match
            # Check if match already exists
            existing_match = Match.find_by_users(current_user_id, swiped_user_id)
            
            if existing_match:
                match_dict = Match.to_dict(existing_match)
                return {
                    'message': 'Match already exists',
                    'match': match_dict,
                    'is_new_match': False
                }, 200
            
            # Delete the existing swipe_right from B->A before creating match
            SwipeRight.delete_by_users(swiped_user_id, current_user_id)
            
            # Create new match
            match = Match.create(current_user_id, swiped_user_id)
            match_dict = Match.to_dict(match)
            
            return {
                'message': 'It\'s a match!',
                'match': match_dict,
                'is_new_match': True
            }, 201
        else:
            # No mutual swipe - save swipe right relationship
            # Check if swipe already exists
            existing_swipe = SwipeRight.find_by_users(current_user_id, swiped_user_id)
            
            if existing_swipe:
                swipe_dict = SwipeRight.to_dict(existing_swipe)
                return {
                    'message': 'Swipe right already recorded',
                    'swipe': swipe_dict
                }, 200
            
            # Create new swipe right
            swipe = SwipeRight.create(current_user_id, swiped_user_id)
            swipe_dict = SwipeRight.to_dict(swipe)
            
            return {
                'message': 'Swipe right recorded',
                'swipe': swipe_dict
            }, 201
            
    except Exception as e:
        return {'error': f'Failed to process swipe right: {str(e)}', 'status_code': 500}, 500


def get_user_matches(current_user_id):
    """
    Get all matches for the current user with matched user information
    Args:
        current_user_id: Current user ID string
    Returns:
        tuple: (response_dict, status_code)
    """
    # Verify current user exists
    user = User.find_by_id(current_user_id)
    if not user:
        return {'error': 'User not found', 'status_code': 404}, 404
    
    try:
        # Get all matches for the user
        matches = Match.find_all_by_user(current_user_id)
        
        # Build matches list with matched user information
        matches_list = []
        for match in matches:
            match_dict = Match.to_dict(match)
            
            # Determine which user is the matched user (the other one)
            if match_dict['user_id_1'] == current_user_id:
                matched_user_id = match_dict['user_id_2']
            else:
                matched_user_id = match_dict['user_id_1']
            
            # Get matched user information
            matched_user = User.find_by_id(matched_user_id)
            if matched_user:
                matched_user_dict = User.to_dict(matched_user)
                matches_list.append({
                    'match_id': match_dict['_id'],
                    'matched_user': matched_user_dict,
                    'created_at': match_dict['created_at']
                })
        
        return {
            'matches': matches_list,
            'count': len(matches_list)
        }, 200
        
    except Exception as e:
        return {'error': f'Failed to get matches: {str(e)}', 'status_code': 500}, 500

