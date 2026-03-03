# QwizzLearn API

QwizzLearn is a backend API for creating, managing, and applying quizzes. Built with FastAPI, it provides a modern, asynchronous web framework for handling quiz-related operations, user authentication, and database interactions. The application is designed to be scalable, secure, and easy to deploy using Docker.

Currently, the API focuses on authentication features, with plans for expansion to core quiz functionalities such as quiz creation, question management, and result tracking.

## Features

- **User Authentication**: Secure JWT-based authentication for user registration, login, and session management.
- **Database Management**: Uses PostgreSQL with SQLModel for ORM and Alembic for migrations.
- **API Endpoints**: Health checks, root welcome message, and authentication routes under `/api/v1/auth`.
- **Logging and Error Handling**: Custom logging for requests/responses/exceptions and dedicated handlers for validation, duplicate entries, and internal errors.
- **CORS Support**: Configured for frontend integration (e.g., allowing origins from localhost and specified frontend URLs).
- **Containerization**: Dockerized setup with Docker Compose for easy development and deployment, including PostgreSQL and Adminer for database administration.
- **Security Best Practices**: Non-root user in Docker, environment variable management, and password hashing with Passlib.

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (async with asyncpg), SQLModel, SQLAlchemy
- **Authentication**: PyJWT, python-jose, Passlib
- **Migrations**: Alembic
- **Configuration**: Pydantic Settings, python-dotenv
- **Server**: Uvicorn
- **Other**: Custom logging, exception handling, CORS middleware
- **Deployment**: Docker, Docker Compose

## Prerequisites

- Docker and Docker Compose (for containerized setup)
- Python 3.12+ (for local development)
- PostgreSQL (if running without Docker)

## Installation

### Using Docker Compose (Recommended)

1. Clone the repository:
   ```
   git clone https://github.com/davidshare/qwizzlearn.git
   cd qwizzlearn
   ```

2. Copy the sample environment file and update with your values:
   ```
   cp .env.sample .env
   ```
   - Update `DB_USER`, `DB_PASS`, `DB_NAME`, etc., as needed.
   - Set a strong `JWT_SECRET_KEY`.

3. Build and start the services:
   ```
   docker-compose up -d --build
   ```

4. Apply database migrations (from inside the container or locally):
   ```
   docker exec -it qwizzlearn alembic upgrade head
   ```

The API will be available at `http://localhost:8001`.  
Adminer (DB management) at `http://localhost:8080`.

### Local Development

1. Clone the repository (as above).

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables (copy and edit `.env.sample` to `.env`).

4. Initialize the database:
   ```
   alembic upgrade head
   ```

5. Run the server:
   ```
   python runserver.py
   ```

The API will run at `http://localhost:8000`.

## Usage

### API Endpoints

- **Root**: `GET /` - Welcome message.
- **Health Check**: `GET /health` - Check API status.
- **Authentication**:
  - Routes under `/api/v1/auth` (e.g., login, register, token refresh). Refer to the code in `app/modules/authentication/routes/v1.py` for details.

Use tools like Postman or curl to interact with the API. For example:
```
curl http://localhost:8001/health
```

### Database Migrations

To create a new migration:
```
alembic revision --autogenerate -m "description"
```
Then apply:
```
alembic upgrade head
```

## Project Structure

- `app/`: Main application code.
  - `core/`: Core utilities (config, database, exceptions, logger, middleware).
  - `modules/`: Feature modules (e.g., `authentication/` for auth logic and routes).
  - `main.py`: FastAPI app setup and entry point.
- `migrations/`: Alembic migration scripts.
- `runserver.py`: Script to start Uvicorn server.
- `requirements.txt`: Python dependencies.
- `docker-compose.yaml`: Defines services (app, DB, Adminer).
- `Dockerfile`: Builds the app container.
- `.env.sample`: Sample environment configuration.
- `alembic.ini`: Alembic configuration.

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -m "Add new feature"`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Open a Pull Request.

Focus areas for improvement:
- Implementing quiz creation and management modules.
- Adding unit/integration tests.
- Frontend integration (e.g., React app).
- Enabling Redis for caching (currently commented out).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details (add one if not present).

## Contact

For questions or feedback, reach out to [davidshare](https://github.com/davidshare).
