# Music Dating App Backend

A Flask-based backend API for a music-based dating application. This backend handles user registration, authentication, profile management, and playlist creation.

## Tech Stack

- **Framework**: Python Flask
- **Database**: MongoDB (MongoDB Atlas)
- **Authentication**: JWT (PyJWT)
- **Password Hashing**: bcrypt
- **Containerization**: Docker

## Project Structure

```
ordinario-ing-software/
├── app/
│   ├── __init__.py          # Flask app initialization
│   ├── config.py             # Configuration settings
│   ├── models/               # Database models
│   │   ├── user.py
│   │   └── playlist.py
│   ├── controllers/          # Business logic
│   │   ├── auth_controller.py
│   │   ├── profile_controller.py
│   │   └── playlist_controller.py
│   ├── routes/               # Route handlers
│   │   ├── auth.py
│   │   ├── profile.py
│   │   └── playlist.py
│   ├── middleware/           # Authentication middleware
│   │   └── auth_middleware.py
│   └── utils/                # Helper functions
│       ├── jwt_utils.py
│       └── validators.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env
```

## Setup Instructions

### Prerequisites

- Python 3.11+
- MongoDB Atlas account (or local MongoDB)
- Docker (optional, for containerized deployment)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ordinario-ing-software
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Update the following variables:
     - `MONGODB_URI`: Your MongoDB Atlas connection string
     - `JWT_SECRET_KEY`: A strong random secret key for JWT signing

5. **Run the application**
   ```bash
   python -m flask run --port 5001
   # Or
   gunicorn --bind 0.0.0.0:5001 app:app
   ```

### Docker Setup

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Or build and run with Docker directly**
   ```bash
   docker build -t music-dating-backend .
   docker run -p 5001:5001 --env-file .env music-dating-backend
   ```

The API will be available at `http://localhost:5001`

## API Endpoints

### Authentication

#### Register User
- **POST** `/api/auth/register`
- **Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "password123",
    "favorite_songs": ["Song 1", "Song 2"],
    "favorite_artists": ["Artist 1", "Artist 2"],
    "favorite_genres": ["Pop", "Rock"],
    "spotify_username": "spotify_user"
  }
  ```
- **Response**: `{message: "User registered successfully", user_id: "..."}`

#### Login
- **POST** `/api/auth/login`
- **Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
- **Response**: `{token: "jwt_token", user_id: "...", email: "user@example.com"}`

### Profile (JWT Protected)

#### Get Profile
- **GET** `/api/profile`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: User profile (excluding password)

#### Update Profile
- **PUT** `/api/profile`
- **Headers**: `Authorization: Bearer <token>`
- **Body** (all fields optional):
  ```json
  {
    "favorite_songs": ["New Song"],
    "favorite_artists": ["New Artist"],
    "favorite_genres": ["Jazz"],
    "spotify_username": "new_spotify_user"
  }
  ```

### Playlist (JWT Protected)

#### Create/Update Playlist
- **POST** `/api/playlist`
- **Headers**: `Authorization: Bearer <token>`
- **Body**:
  ```json
  {
    "songs": [
      {"song_name": "Song 1", "artist_name": "Artist 1"},
      {"song_name": "Song 2", "artist_name": "Artist 2"},
      ... (exactly 10 songs)
    ]
  }
  ```

#### Get Playlist
- **GET** `/api/playlist`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: User's top 10 playlist

## Testing with Postman

1. Import the API endpoints into Postman
2. For protected routes, first call `/api/auth/login` to get a JWT token
3. Copy the token from the response
4. In subsequent requests, add header: `Authorization: Bearer <your_token>`

## Error Responses

All errors follow this format:
```json
{
  "error": "Error message",
  "status_code": 400
}
```

Common status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `404`: Not Found
- `500`: Internal Server Error
