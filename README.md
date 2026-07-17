# VIBRANTIC AGENTIC CHATBOT

An enterprise-grade SaaS platform for building, deploying, and managing AI-powered chatbots and intelligent agents.

## Tech Stack

### Backend

* Python 3.12+
* FastAPI
* SQLAlchemy
* PostgreSQL
* Alembic
* Pydantic
* JWT Authentication
* Loguru
* Pytest
* UV Package Manager

### Frontend

* HTML
* CSS
* JavaScript

---

# Project Structure

```text
VIBRANTIC_AGENTIC_CHATBOT/
│
├── backend/
│   ├── alembic/
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── dependencies/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── seeders/
│   ├── services/
│   ├── templates/
│   ├── tests/
│   ├── main.py
│   ├── pyproject.toml
│   └── uv.lock
│
├── ui/
│
└── README.md
```

---

# Prerequisites

Install:

* Python 3.12 or newer
* PostgreSQL
* Git
* UV

Install UV if needed:

```bash
pip install uv
```

---

# Clone the Repository

```bash
git clone <repository-url>
cd VIBRANTIC_AGENTIC_CHATBOT
```

---

# Backend Setup

Move into the backend directory.

```bash
cd backend
```

Create a virtual environment.

```bash
uv venv
```

Activate it.

### Windows

```powershell
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies.

```bash
uv sync
```

---

# Environment Variables

Create a `.env` file inside the `backend` directory.

Example:

```env
APP_NAME=Vibrantic Agentic Chatbot
DEBUG=True

DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/vibrantic_ai

SECRET_KEY=your-secret-key

ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

# Database Migration

Run all migrations.

```bash
uv run alembic upgrade head
```

Create a new migration.

```bash
uv run alembic revision --autogenerate -m "description"
```

---

# Seed Sample Data

```bash
uv run python -m seeders.run_seeders
```

---

# Run the Development Server

```bash
uv run uvicorn main:app --reload
```

Default API URL:

```
http://127.0.0.1:8000
```

Swagger Documentation:

```
http://127.0.0.1:8000/docs
```

ReDoc:

```
http://127.0.0.1:8000/redoc
```

---

# Running Tests

Run all tests.

```bash
uv run pytest
```

Run with coverage.

```bash
uv run pytest --cov
```

---

# Useful Commands

Install a package.

```bash
uv add package-name
```

Remove a package.

```bash
uv remove package-name
```

Update dependencies.

```bash
uv sync
```

Show installed packages.

```bash
uv pip list
```

---

# Git Workflow

Check status.

```bash
git status
```

Stage changes.

```bash
git add .
```

Commit.

```bash
git commit -m "Your commit message"
```

Push.

```bash
git push origin main
```

---

# Current Features

* Authentication
* Organizations
* Members
* Invitations
* Role-Based Access Control (RBAC)
* Email Invitations
* Database Migrations (Alembic)
* Seeders
* Repository Pattern
* Service Layer
* Unit of Work
* Centralized Logging
* Exception Handling
* Automated Testing

---

# License

This project is intended for educational and commercial development purposes.
