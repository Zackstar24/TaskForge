# TaskForge Project Context & Development Handoff

## About the Developer

The developer is a recent Computer Science bachelor's graduate looking to transition into software engineering.

Background:

* Bachelor's degree in Computer Science
* Primary programming languages learned:

  * C++
  * Python
* No professional CS work experience yet
* Has been away from coding for approximately one year and is rebuilding confidence and skills

Career goal:

* Obtain an entry-level software engineering/backend/full-stack development role
* Build portfolio projects that demonstrate real-world engineering ability
* Create projects that are more impressive than simple tutorials or school assignments

The developer prefers:

* Understanding why things are done, not just copying commands
* Step-by-step guidance
* Explanations of concepts and architecture
* Learning professional workflows used by real developers

When teaching:

* Explain what each tool does
* Explain why decisions are made
* Avoid treating commands as magic
* Confirm terminal output before moving forward

---

# Main Project

## Name

TaskForge

## Purpose

TaskForge is a full-stack task management application designed as a portfolio project.

The goal is to build a realistic application that demonstrates:

* Backend development
* Frontend development
* Database design
* REST APIs
* Authentication
* Git/GitHub workflow
* Testing
* Deployment
* Real software engineering practices

The final goal is for TaskForge to become a real application that other people can use.

Long-term vision:

A friend should eventually be able to:

1. Visit a website
2. Create an account
3. Log in
4. Create and manage personal tasks
5. Use the application from anywhere

---

# Current Development Environment

The computer was recently reformatted, so the development environment was rebuilt from scratch.

Installed:

* VS Code
* Python 3.14.6
* Git 2.55.0.windows.2

Operating system:

* Windows

Terminal:

* PowerShell inside VS Code

Project location:

```
D:\SoftwarePortfolio\TaskForge
```

---

# Current Project Structure

Current structure:

```
TaskForge
│
├── .venv/
│
├── backend/
│   └── main.py
│
├── .gitignore
│
├── requirements.txt
│
└── DEVELOPMENT_LOG.md
```

---

# Python Environment

A virtual environment was created:

```
py -m venv .venv
```

PowerShell initially blocked activation scripts.

Fixed using:

```
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Virtual environment activation:

```
.\.venv\Scripts\Activate.ps1
```

The terminal should show:

```
(.venv)
```

when active.

---

# Backend Setup

FastAPI and Uvicorn were installed:

```
pip install fastapi uvicorn
```

Dependencies saved:

```
pip freeze > requirements.txt
```

Current backend entry file:

```
backend/main.py
```

Current code:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "TaskForge backend is running!"}
```

---

# Running the Backend

The backend currently runs with:

```
uvicorn backend.main:app --reload
```

Successful test:

Opening:

```
http://127.0.0.1:8000
```

returns:

```json
{
    "message": "TaskForge backend is running!"
}
```

This was the first successful application milestone.

---

# Git Setup

Git was initialized:

```
git init
```

Branch renamed:

```
git branch -M main
```

GitHub repository:

```
https://github.com/Zackstar24/TaskForge.git
```

The repository is connected and pushed successfully.

---

# Git Workflow

The developer understands that:

Saving files ≠ uploading them.

The workflow should be:

```
Write code
↓
Save files
↓
git status
↓
git add .
↓
git commit -m "Description"
↓
git push
```

Before finishing each coding session:

1. Update DEVELOPMENT_LOG.md
2. Save changes
3. Commit progress
4. Push to GitHub

---

# Git Ignore

The project ignores:

```
.venv/
__pycache__/
*.pyc
```

Reason:

* Virtual environments should not be uploaded
* Python cache files are generated automatically

---

# Development Log

A major goal is maintaining a daily development journal.

File:

```
DEVELOPMENT_LOG.md
```

The developer wants to update this every time they work on the project.

Each entry should include:

## Date

Example:

```
## July 10, 2026
```

## Completed

Things finished during the session.

Example:

```
- Installed FastAPI
- Created backend server
- Connected GitHub repository
```

## Learned

Concepts understood.

Example:

```
- Learned how virtual environments work
- Learned Git commit workflow
```

## Next Goals

Future tasks.

Example:

```
- Add database
- Learn SQLAlchemy
- Create Task model
```

The development log should be treated as an important part of the project.

At the end of every session, remind the developer:

"Update DEVELOPMENT_LOG.md before committing."

---

# Current Development Log Roadmap

The developer wants a long-term checklist that items can move from "Next Goals" to "Completed."

## Backend Foundation

* Improve backend project structure
* Learn SQLAlchemy ORM
* Add SQLite database
* Create database connection
* Create database models
* Create Task model
* Create User model
* Learn database migrations
* Implement CRUD operations
* Create FastAPI routers
* Add Pydantic schemas

---

## Task Features

* Create tasks
* View tasks
* Edit tasks
* Delete tasks
* Complete tasks
* Add priorities
* Add categories
* Add due dates
* Add filtering
* Add sorting
* Add search

---

## Authentication

* Learn authentication concepts
* Create registration system
* Create login system
* Hash passwords
* Implement JWT authentication
* Protect user routes
* Connect tasks to users
* Create user profiles

---

## Frontend

Recommended technology:

React

Goals:

* Create frontend project
* Build login page
* Build registration page
* Build dashboard
* Connect frontend to backend
* Display tasks
* Create task forms
* Add responsive design

---

## Full Stack Integration

* Connect frontend and backend
* Handle API requests
* Handle authentication state
* Add validation
* Improve user experience

---

## Professional Engineering Practices

* Maintain Git history
* Write documentation
* Create strong README
* Document APIs
* Learn environment variables
* Add testing
* Write unit tests
* Write integration tests
* Improve debugging skills

---

## Security

* Learn web security basics
* Secure authentication
* Protect user data
* Validate input
* Prevent common vulnerabilities

---

## Deployment

Eventually:

* Prepare production build
* Deploy backend
* Deploy frontend
* Set up production database
* Configure environment variables
* Create public URL
* Allow friends to use TaskForge

---

# Future Features

Possible advanced features:

* Shared task lists
* Team workspaces
* Comments
* File attachments
* Notifications
* Calendar integration
* Activity history
* User settings
* Dark mode
* AI task suggestions
* Mobile application

---

# Immediate Next Steps

The project should continue with:

## Sprint 2: Backend Foundation

Tasks:

1. Clean up backend architecture
2. Introduce SQLAlchemy
3. Create database connection
4. Create Task database model
5. Create CRUD endpoints
6. Learn how FastAPI interacts with databases

---

# Important Guidance

This is a learning project, but it should be built like a professional project.

Prioritize:

* Understanding concepts
* Good architecture
* Clean Git history
* Documentation
* Incremental progress

Do not rush to add advanced features.

The most valuable portfolio version is:

✅ FastAPI backend
✅ Database
✅ User accounts
✅ Authentication
✅ CRUD task system
✅ Frontend
✅ Deployment

A completed version of that is already a strong entry-level software engineering portfolio project.

---

# Current Status

Completed:

✅ Development environment setup
✅ Python installation
✅ Git installation
✅ VS Code setup
✅ GitHub repository
✅ Virtual environment
✅ FastAPI installation
✅ Backend server
✅ First API endpoint
✅ requirements.txt
✅ .gitignore
✅ Initial Git commits
✅ Development workflow established

Current milestone:

TaskForge backend foundation complete.

Next session should continue with database/backend architecture.
