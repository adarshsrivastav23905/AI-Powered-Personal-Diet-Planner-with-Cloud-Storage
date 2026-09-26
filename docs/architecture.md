# Architecture Overview

## High-Level Flow

User
  ↓
React Frontend
  ↓
JWT Authentication
  ↓
Flask REST API
  ↓
┌──────────────────────────────┐
│ AI Diet Recommendation      │
│ Engine / Nutrition Service   │
└──────────────────────────────┘
  ↓
SQLite Database (simulated cloud database)
  ↓
Local Storage Simulation (user-scoped files)
  ↓
Dashboard, plans, profile, uploads

## Components

### Frontend
The frontend is built with React and Vite. It handles user interactions such as:

- sign up and login
- profile details
- diet plan generation
- viewing previous plans
- uploading files

### Backend
The Python Flask backend exposes REST endpoints to manage:

- authentication
- profile updates
- nutrition targets
- plan generation
- file upload workflows

### AI Engine
The AI engine uses a rule-based planner that incorporates:

- dietary preferences
- calories and macros
- activity level
- goal type
- allergies

### Database
The project uses SQLite for local simulation of a cloud database. It stores:

- users
- diet plans
- files metadata

### Storage Layer
Files are stored in a user-specific folder to simulate cloud object storage. It demonstrates how unstructured files differ from database records.

## Data Flow

1. User creates an account.
2. User completes the profile.
3. Backend validates inputs.
4. Backend calculates nutrition targets.
5. AI engine produces plan based on user preferences.
6. Plan is stored in the database.
7. User can upload files or save plans.
8. Frontend retrieves and displays user-specific data.

## Cloud Concepts Covered

- Client-server architecture
- Authentication and authorization
- API-driven communication
- User data isolation
- Cloud database design
- Object storage simulation
- Deployment-ready project structure
