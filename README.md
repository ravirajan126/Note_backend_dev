#Notes App – FastAPI Backend

This is a simple notes-taking backend API built with FastAPI and PostgreSQL. It supports user registration, login, and note management (create, view, update, delete).
#How to Install and Run Locally

1. Clone the repository
   Make sure this project is in a clean, new directory.

2. Set up a Python environment
   python -m venv venv
   source venv/bin/activate
   # Windows: venv\Scripts\activate
3. Install required packages
   pip install -r requirements.txt
4. change .env file in the project root:
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=notes_db
   DB_USER=postgres
   DB_PASSWORD=yourpassword
   SECRET_KEY=your-secret-key
5. Start the server
   uvicorn app.main:app --reload
6. Visit your API docs at:
   Swagger UI: http://localhost:8000/docs


Design Decisions & Trade-offs
  Chose FastAPI for fast development, async support, and automatic docs.
  Used UUIDs for user and note IDs to ensure global uniqueness and security.
  JWT authentication for stateless login with secure access to user data.

