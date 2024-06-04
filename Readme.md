# ChatAPI

A robust API for managing chat rooms and messages using Django Rest Framework, PostgreSQL, and Docker. This application supports high request volumes, and efficient search functionality.

## Features

- **Chat Room Management**: Create, update, and read chat rooms.
- **Message Management**: Create, update, and read messages within chat rooms.
- **Search**: Search messages within a specific chat room, user or by partial match of the message content using postgresql full text search.
- **User Management**: Secure endpoints with authentication.
- **Containerization**: Easily deploy the application using Docker.

## Endpoints

### Chat Rooms

- **Create Chat Room**: `POST /rooms/`
- **Update Chat Room**: `PUT /rooms/<int:pk>/`
- **Read Chat Room**: `GET /rooms/<int:pk>/`
- **List Chat Rooms**: `GET /rooms/`

### Messages

- **Create Message**: `POST /messages/`
- **Update Message**: `PUT /messages/<int:pk>/`
- **Read Message**: `GET /messages/<int:pk>/`
- **List Messages**: `GET /messages/`
- **Search Messages**: `GET /messages/?search=<query>`
- ***messages can be filtered by room or user ?room=<room_id>?user=<user_id>***

## Permissions

### Room Permissions

- **IsRoomUserOrAdmin**: This permission class ensures that only users who are part of a room or the room admin can perform actions on the room. Specifically:
  - For safe methods (GET, HEAD, OPTIONS), any user who is a member of the room can access the room details.
  - For unsafe methods (PUT, DELETE), only the admin of the room can perform the action.

### Message Permissions

- **IsMessageOwnerOrReadOnly**: This permission class ensures that only the user who created the message can modify or delete it. Specifically:
  - For safe methods (GET, HEAD, OPTIONS), any user can access the message details (user can only view masseges from rooms he is a member of).
  - For unsafe methods (PUT, DELETE), only the user who created the message can perform

## Performance

### Indexing

- An index is created for the created_at and updated_at fields of messages to facilitate efficient ordering.
- For the message content, an index would improve the performance of text search but slow down write operations. Thus, content indexing is not implemented to balance performance.

### Counts

- The count of rooms and messages could be updated every hour using Redis for caching. However, pagination is preferred to improve overall performance, eliminating the need for real-time counts.

## Technical Requirements

- **API Framework**: Django Rest Framework
- **Database**: PostgreSQL
- **Authentication**: Djoser - JWT (JSON Web Token)
- **Containerization**: Docker

## Installation

### Prerequisites

- Docker and Docker Compose installed on your machine.

### Setup

1. **Clone the repository**:

   ```sh
   git clone https://github.com/oel21sakka/ChatAPI.git
   cd ChatAPI
   ```

2. **Create a `.env` file**:

   ```sh
   touch .env
   ```

   Add the following environment variables to the `.env` file:

   ```sh
   PG_USER=postgres
   PG_PASSWORD=postgres
   PG_DB=postgres
   PG_PORT=5432
   PG_HOST=db
   ```

3. **Build and run the application**:

   ```sh
   docker-compose up --build
   ```

4. **Apply migrations**:

   Migrations will be applied automatically by the entrypoint script included in the Docker setup.

5. **Access the application**:

   The API will be available at `http://localhost:8000/`.

### Admin User

To create a superuser for accessing the Django admin interface:

1. **Run the Django container interactively**:

   ```sh
   docker-compose run djangoapp python3 manage.py createsuperuser
   ```

2. **Follow the prompts to create the superuser.**

3. **Access the admin interface** at `http://localhost:8000/admin/`.

## Testing

    - You will find a Postman collection containing unit tests for the endpoints.

## API Documentation

This API follows RESTful principles. Below are some key endpoints:

- **User Authentication**:

  - Obtain Token: `POST /auth/jwt/create/`
  - Refresh Token: `POST /auth/jwt/refresh/`
  - Verify Token: `POST /auth/jwt/verify/`

- **Chat Rooms**:

  - Create: `POST /rooms/`
  - Update: `PUT /rooms/<int:pk>/`
  - Retrieve: `GET /rooms/<int:pk>/`
  - List: `GET /rooms/`

- **Messages**:
  - Create: `POST /messages/`
  - Update: `PUT /messages/<int:pk>/`
  - Retrieve: `GET /messages/<int:pk>/`
  - List: `GET /messages/`
  - Search: `GET /messages/?search=<query>`

## Further work

- **Add WebSockets to Handle Messages in Real-time**

- **Use Redis Caching to Improve Performance**
