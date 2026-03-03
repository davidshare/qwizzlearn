# QwizzLearn API

**QwizzLearn** is a high-performance, asynchronous REST API built with **FastAPI**. It serves as the backbone for an educational platform, handling quiz orchestration, user progress tracking, and automated assessment logic with speed and type safety.

## 🛠️ Tech Stack

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python)
* **Asynchronous ORM:** SQLAlchemy (with `asyncio`) or Tortoise ORM
* **Data Validation:** [Pydantic v2](https://www.google.com/search?q=https://docs.pydantic.dev/)
* **Database:** PostgreSQL (Recommended)
* **Authentication:** JWT (JSON Web Tokens) with OAuth2 Password Flow
* **Environment Management:** Python-dotenv

## Core Features

* **Async Performance:** Leveraging Python's `async/await` for high-concurrency quiz sessions.
* **Automated Documentation:** Interactive API docs via Swagger UI and ReDoc.
* **Strict Typing:** Full Pydantic integration for request/response validation.
* **User Authentication:** Secure password hashing and token-based authorization.
* **Quiz Management:** CRUD operations for questions, categories, and user responses.

## Prerequisites

* Python 3.9 or higher
* PostgreSQL (or your preferred SQL database)
* Virtual environment (venv/pipenv/poetry)

## Installation & Setup

1. **Clone the repository:**
```bash
git clone https://github.com/davidshare/qwizzlearn.git
cd qwizzlearn

```


2. **Set up a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

```


3. **Install dependencies:**
```bash
pip install -r requirements.txt

```


4. **Environment Configuration:**
Create a `.env` file in the root directory:
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost/qwizzlearn
SECRET_KEY=your_super_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

```


5. **Run the Server:**
```bash
uvicorn app.main:app --reload

```



## 📖 API Documentation

Once the server is running, you can access the interactive documentation at:

* **Swagger UI:** [http://127.0.0.1:8000/docs](https://www.google.com/search?q=http://127.0.0.1:8000/docs)
* **ReDoc:** [http://127.0.0.1:8000/redoc](https://www.google.com/search?q=http://127.0.0.1:8000/redoc)

## Project Structure

```text
├── app
│   ├── api          # API route handlers (endpoints)
│   ├── core         # Configuration, security, and global constants
│   ├── models       # Database schemas (SQLAlchemy/Tortoise)
│   ├── schemas      # Pydantic models (Request/Response validation)
│   ├── crud         # Create, Read, Update, Delete logic
│   └── main.py      # Entry point of the FastAPI application
├── tests            # Pytest suite
├── .env             # Environment variables
└── requirements.txt # Project dependencies

```

## Testing

To run the test suite using `pytest`:

```bash
pytest

```

## Contributing

1. Fork the Project.
2. Create your Feature Branch (`git checkout -b feature/NewEndpoint`).
3. Commit your Changes (`git commit -m 'Add some NewEndpoint'`).
4. Push to the Branch (`git push origin feature/NewEndpoint`).
5. Open a Pull Request.

## License

Distributed under the MIT License. See `LICENSE` for more information.

---

**Developed by [David Itam Essien**](https://github.com/davidshare)
