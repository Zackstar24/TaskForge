# TaskForge Development Log

## July 10, 2026

### Completed
- Set up development environment from scratch
- Installed Python 3.14.6
- Installed Git and configured GitHub integration
- Created TaskForge project repository
- Initialized Git version control
- Created Python virtual environment
- Installed FastAPI and Uvicorn
- Created first FastAPI backend endpoint
- Successfully ran local backend server
- Added requirements.txt
- Added .gitignore
- Published repository to GitHub
- Added GET /tasks endpoint to retrieve all tasks
- Added GET /tasks/{task_id} endpoint to retrieve a single task
- Added validation requiring task IDs to be greater than or equal to 1
- Added a 404 Not Found response for tasks that do not exist
- Verified task retrieval and error responses through PowerShell

## July 13, 2026

### Completed
- Converted the backend directory into a Python package
- Installed and configured SQLAlchemy
- Created the SQLite database connection and session system
- Created the Task database model
- Configured FastAPI to create database tables during application startup
- Added Pydantic schemas for task creation and API responses
- Created the first task CRUD operation
- Created the POST /tasks API endpoint using a FastAPI router
- Verified that tasks are validated, saved to SQLite, and returned by the API

## July 15, 2026

### Completed
- Completed database-backed CRUD operations for tasks
- Added endpoints to create, retrieve, update, complete, and delete tasks
- Added Pydantic validation for task creation and partial updates
- Added proper 404, 422, 201, and 204 API responses
- Added and configured Alembic for database schema migrations
- Created and tested the initial tasks-table migration
- Brought the existing SQLite database under Alembic migration control without losing task data

## July 20, 2026

- Added an automated testing environment using pytest, FastAPI TestClient, and an isolated in-memory SQLite database
- Created API integration tests covering task creation, retrieval, updates, deletion, validation, and error responses
- Added task priority support with low, medium, and high values
- Added medium as the default priority for new and existing tasks
- Updated the task database model, Pydantic schemas, and API responses to support priorities
- Created and applied an Alembic migration for the new priority column
- Identified and corrected a duplicate SQLite priority constraint before committing the migration
- Added tests for default, explicit, invalid, updated, and null priority values
- Debugged duplicate test-helper code and restored the complete CRUD test coverage
- Verified that all 16 automated tests pass and that the database schema matches the SQLAlchemy models

## July 29, 2026

- Initialized the React and TypeScript frontend with Vite
- Verified the frontend development server, linting, and production build
- Configured FastAPI CORS access for the local React frontend
- Connected React to the FastAPI task API
- Added loading, error, empty, and populated task-list states
- Created TypeScript models and a dedicated frontend API client
- Added a controlled form for creating tasks in the browser
- Verified that newly created tasks persist in SQLite after refresh
- Added controls for completing, reopening, and deleting tasks
- Added per-task request states, deletion confirmation, and error feedback
- Extracted task rendering and actions into a reusable TaskCard component
- Verified backend tests and frontend production checks

## July 30, 2026

- Added inline editing for task titles, descriptions, and priorities
- Added controlled edit inputs with save, cancel, validation, and request states
- Reused the existing PATCH API integration to persist task changes
- Verified edited task values persist after browser refresh
- Verified frontend linting, production build, and backend tests

## August 6, 2026

- Added a User database model with unique normalized email addresses
- Added secure Argon2 password hashing and verification utilities
- Created the user registration endpoint with validation and duplicate-email handling
- Added and applied an Alembic migration for the users table
- Added registration tests covering email normalization, password hashing, invalid input, response security, and duplicate accounts
- Verified all 21 automated tests pass and the database schema matches the SQLAlchemy models

## August 7, 2026

- Added JWT-based user login with signed, expiring access tokens
- Added secure credential verification using stored Argon2 password hashes
- Added authenticated current-user resolution from bearer tokens
- Created the protected `/auth/me` endpoint
- Added consistent 401 responses for invalid credentials, missing tokens, and invalid tokens
- Added environment-based JWT secret configuration so application secrets are not stored in source control
- Added authentication tests covering login, token issuance, current-user access, invalid credentials, and invalid tokens
- Verified all 28 automated tests pass with no dependency or database schema issues
- Added authenticated task ownership with a user-to-task relationship
- Added a reversible Alembic migration linking tasks to users while preserving legacy tasks
- Scoped task creation, listing, retrieval, updates, and deletion to the authenticated user
- Added authorization tests verifying users only see their own tasks and cannot access another user's tasks
- Verified the ownership migration upgrades and downgrades without data loss
- Verified all 31 automated tests pass

## August 9, 2026

- Added frontend authentication types for users, registration, login, and JWT token responses
- Added a shared API client with centralized bearer-token handling
- Added browser access-token storage and logout support
- Added frontend registration, login, and current-user API functions
- Refactored the task API client to use authenticated requests
- Added environment-based frontend API URL configuration for deployment
- Verified frontend linting and production build pass
- Added frontend registration and login interface
- Added automatic login after registration
- Added authenticated session restoration across page refreshes
- Added logout functionality and authenticated dashboard access
- Added user-friendly registration, login, and network error messages
- Persisted the local JWT development secret outside source control
- Verified frontend linting and production build pass
- Verified all 31 backend tests pass
- Manually verified task creation, session restoration, logout, and login persistence
- Added environment-based database configuration with SQLite as the local development fallback
- Added PostgreSQL support using Psycopg 3 for production deployment
- Updated Alembic to use the same database configuration as the application
- Added database URL normalization for PostgreSQL connection strings
- Added automated tests for SQLite fallback and PostgreSQL configuration
- Verified SQLAlchemy correctly selects the PostgreSQL Psycopg driver
- Verified all 34 automated tests pass with no dependency or schema issues
- Provisioned a managed PostgreSQL database on Render and successfully applied the full Alembic migration history.
- Verified TaskForge locally against the Render PostgreSQL database, including registration, authentication, task creation, and persistence.
- Deployed the FastAPI backend to Render and verified the public API, Swagger documentation, JWT authentication, and authenticated task operations.
- Deployed the React frontend to Render at https://taskforge-zack.onrender.com.
- Added environment-driven production CORS configuration while preserving localhost development origins.
- Added CORS configuration coverage and verified the full backend test suite with 35 passing tests.

## Checklist:

### Backend Foundation
- [x] Improve backend project structure
- [x] Learn and implement SQLAlchemy ORM
- [x] Set up SQLite database
- [x] Create database connection system
- [x] Create database models
- [x] Create Task model
- [ ] Create User model
- [x] Learn database migrations
- [x] Implement CRUD operations for tasks
- [x] Create API routes using FastAPI routers
- [x] Add API request validation with Pydantic schemas
- [x] Create initial Alembic database migration

### Task Management Features
- [x] Create tasks
- [x] View tasks
- [x] Update tasks
- [x] Delete tasks
- [x] Mark tasks as completed
- [x] Add task priorities
- [ ] Add task categories/tagsD
- [ ] Add due dates
- [ ] Add task filtering and sorting
- [ ] Add search functionality

### User Accounts & Authentication
- [ ] Learn authentication concepts
- [ ] Create user registration system
- [ ] Create login system
- [ ] Implement password hashing
- [ ] Implement JWT authentication
- [ ] Protect user-specific API routes
- [ ] Connect tasks to individual users
- [ ] Create user profile system

### Frontend Development
- [x] Set up the React, TypeScript, and Vite frontend environment
- [x] Configure linting, production builds, and local CORS
- [x] Create a typed API client and connect React to FastAPI
- [x] Build the task dashboard with loading, error, empty, and populated states
- [x] Display task details, priorities, and completion status
- [x] Create tasks with validation, submission feedback, and database persistence
- [x] Complete, reopen, and delete tasks with confirmation and per-task request states
- [x] Organize the interface into reusable components and synchronize frontend state with API responses
- [x] Create the task editing interface
- [ ] Complete and test responsive mobile design
- [ ] Build registration and login interfaces
- [ ] Continue developing React fundamentals through implementation

### Full-Stack Integration
- [x] Connect frontend and backend together
- [x] Handle API requests from frontend
- [ ] Handle user sessions
- [x] Handle frontend errors
- [x] Add loading states
- [ ] Improve user experience
- [ ] Add form validation

### Software Engineering Practices
- [ ] Improve Git workflow
- [ ] Maintain meaningful commit messages
- [ ] Write better documentation
- [ ] Create detailed README
- [ ] Add API documentation
- [ ] Learn environment variables
- [ ] Create configuration management
- [x] Add automated testing
- [ ] Write backend unit tests
- [x] Write API integration tests
- [ ] Learn debugging techniques
- [x] Configure an isolated SQLite database for automated tests
- [x] Add automated CRUD and validation test coverage
- [x] Validate task priority values

### Authentication and Authorization

- [x] Add the user model and database migration
- [x] Add secure password hashing
- [x] Add user registration with validation and duplicate-email handling
- [x] Test registration and password storage
- [x] Add JWT login and authenticated-user dependencies
- [x] Protect task routes and assign tasks to users
- [x] Build frontend registration, login, logout, and session handling

### Security Improvements
- [ ] Learn common web security concepts
- [ ] Secure user authentication
- [ ] Protect sensitive data
- [ ] Validate user input
- [ ] Prevent common API vulnerabilities
- [ ] Secure database access

### Deployment
- [ ] Learn cloud deployment basics
- [ ] Prepare application for production
- [ ] Deploy backend server
- [ ] Deploy frontend application
- [ ] Set up production database
- [ ] Configure environment variables
- [ ] Create public URL
- [ ] Allow friends to create accounts and use TaskForge

### Advanced Features (Future Ideas)
- [ ] Add shared task lists
- [ ] Add team/workspace functionality
- [ ] Add task comments
- [ ] Add file attachments
- [ ] Add notifications
- [ ] Add calendar integration
- [ ] Add activity history
- [ ] Add user settings
- [ ] Add dark mode
- [ ] Add AI-powered task suggestions
- [ ] Create mobile application