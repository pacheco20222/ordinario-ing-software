# Postman API Examples

## Base URL
```
http://localhost:5001
```

## 1. Register User

**POST** `/api/auth/register`

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "favorite_songs": ["Bohemian Rhapsody", "Stairway to Heaven"],
  "favorite_artists": ["Queen", "Led Zeppelin"],
  "favorite_genres": ["Rock", "Classic Rock"],
  "spotify_username": "spotify_user123"
}
```

**Expected Response (201):**
```json
{
  "message": "User registered successfully",
  "user_id": "507f1f77bcf86cd799439011"
}
```

## 2. Login

**POST** `/api/auth/login`

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Expected Response (200):**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user_id": "507f1f77bcf86cd799439011",
  "email": "user@example.com"
}
```

**Save the token for protected routes!**

## 3. Get Profile (Protected)

**GET** `/api/profile`

**Headers:**
```
Authorization: Bearer <your_token_here>
Content-Type: application/json
```

**Expected Response (200):**
```json
{
  "_id": "507f1f77bcf86cd799439011",
  "email": "user@example.com",
  "favorite_songs": ["Bohemian Rhapsody", "Stairway to Heaven"],
  "favorite_artists": ["Queen", "Led Zeppelin"],
  "favorite_genres": ["Rock", "Classic Rock"],
  "spotify_username": "spotify_user123",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

## 4. Update Profile (Protected)

**PUT** `/api/profile`

**Headers:**
```
Authorization: Bearer <your_token_here>
Content-Type: application/json
```

**Body (all fields optional):**
```json
{
  "favorite_songs": ["New Song 1", "New Song 2"],
  "favorite_artists": ["New Artist"],
  "favorite_genres": ["Jazz", "Blues"],
  "spotify_username": "new_spotify_user"
}
```

**Expected Response (200):**
```json
{
  "_id": "507f1f77bcf86cd799439011",
  "email": "user@example.com",
  "favorite_songs": ["New Song 1", "New Song 2"],
  "favorite_artists": ["New Artist"],
  "favorite_genres": ["Jazz", "Blues"],
  "spotify_username": "new_spotify_user",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T01:00:00"
}
```

## 5. Create/Update Playlist (Protected)

**POST** `/api/playlist`

**Headers:**
```
Authorization: Bearer <your_token_here>
Content-Type: application/json
```

**Body (exactly 10 songs required):**
```json
{
  "songs": [
    {"song_name": "Song 1", "artist_name": "Artist 1"},
    {"song_name": "Song 2", "artist_name": "Artist 2"},
    {"song_name": "Song 3", "artist_name": "Artist 3"},
    {"song_name": "Song 4", "artist_name": "Artist 4"},
    {"song_name": "Song 5", "artist_name": "Artist 5"},
    {"song_name": "Song 6", "artist_name": "Artist 6"},
    {"song_name": "Song 7", "artist_name": "Artist 7"},
    {"song_name": "Song 8", "artist_name": "Artist 8"},
    {"song_name": "Song 9", "artist_name": "Artist 9"},
    {"song_name": "Song 10", "artist_name": "Artist 10"}
  ]
}
```

**Expected Response (200):**
```json
{
  "_id": "507f1f77bcf86cd799439012",
  "user_id": "507f1f77bcf86cd799439011",
  "songs": [
    {"song_name": "Song 1", "artist_name": "Artist 1"},
    ...
  ],
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

## 6. Get Playlist (Protected)

**GET** `/api/playlist`

**Headers:**
```
Authorization: Bearer <your_token_here>
Content-Type: application/json
```

**Expected Response (200):**
```json
{
  "_id": "507f1f77bcf86cd799439012",
  "user_id": "507f1f77bcf86cd799439011",
  "songs": [
    {"song_name": "Song 1", "artist_name": "Artist 1"},
    ...
  ],
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

## Error Responses

All errors follow this format:

```json
{
  "error": "Error message here",
  "status_code": 400
}
```

### Common Errors:

**401 Unauthorized:**
```json
{
  "error": "Token is missing",
  "status_code": 401
}
```

**400 Bad Request:**
```json
{
  "error": "Playlist must contain exactly 10 songs",
  "status_code": 400
}
```

**404 Not Found:**
```json
{
  "error": "User not found",
  "status_code": 404
}
```

