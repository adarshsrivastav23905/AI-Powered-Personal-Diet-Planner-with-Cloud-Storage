# AI-Powered Personal Diet Planner with Cloud Storage

A modern full-stack cloud-computing project designed to help users plan healthier meals through personalized nutrition recommendations, secure profile management, and a cloud-inspired storage workflow. This application combines a Python Flask backend, React frontend, SQLite-based user data storage, and an AI-style meal planning engine to demonstrate core cloud application principles in a practical, student-friendly project.

## Project Description

NutriCloud AI is a personal diet planner that helps users register, create a health profile, define nutrition goals, and generate custom meal plans based on their preferences and lifestyle. It demonstrates how a real-world web application can integrate authentication, user-specific data storage, API-driven services, and cloud-like file storage into a single project.

The system is designed for accessibility and clarity: users can sign in, update their profile, generate a plan, review meal recommendations, and save or manage personal data through a clean dashboard experience. The project is intentionally structured to be both functional and easy to explain during interviews, presentations, and academic evaluation.

## Overview

This project solves a common real-world problem: people struggle to plan meals consistently, keep track of calories and macros, and stay aligned with personal health goals. The app lets a user:

- register and log in securely
- create a health profile
- set a goal like weight loss, maintain, or gain
- generate a personalized diet plan
- save and retrieve plans
- upload and access files in a cloud-storage-style workflow
- view a modern dashboard experience

This project is designed as a beginner-friendly, GitHub-ready cloud project that can be run locally and explained clearly in interviews.

## Problem Statement

People often do not know which foods match their goals, activity level, and dietary preferences. This leads to inconsistent eating habits and poor planning. A cloud-backed app helps centralize user data, personalize plans, and provide access across devices.

## Objectives

- Build a responsive frontend for user interaction
- Implement a backend API with authentication
- Store user data securely and separately per user
- Generate diet recommendations using a local AI rule-based engine
- Simulate cloud storage with user-scoped uploads
- Demonstrate testing, deployment thinking, and GitHub-ready documentation

## Features

- User registration and login
- JWT-based protected routes
- User profile creation and updates
- Nutrition target calculation (BMR/TDEE/macros)
- Automated diet plan generation
- Vegetarian and vegan support
- Goal-specific plan generation
- Plan retrieval and deletion
- File upload and download simulation
- Secure user isolation
- Testing suite for the backend

## Cloud Computing Concepts Demonstrated

This project includes the following concepts:

- Cloud-hosted web app architecture
- Authentication and authorization
- Cloud database simulation using SQLite
- Object storage simulation with local user folders
- REST API communication between frontend and backend
- Client-server architecture
- Data isolation per user
- Scalability and cloud deployment readiness
- Environment-variable-based configuration
- Security basics and validation

## Technology Stack

### Recommended local setup used in this project

- Frontend: React + Vite
- Backend: Python Flask
- Database: SQLite (local cloud-database simulation)
- AI Engine: Rule-based diet recommendation engine
- Storage: Local object storage simulation
- Authentication: JWT
- Testing: Pytest

## Architecture

User
  ↓
Frontend (React)
  ↓
Authentication
  ↓
REST API (Flask)
  ↓
AI Engine / Nutrition Logic
  ↓
Database (SQLite)
  ↓
Storage Layer (simulated cloud object storage)
  ↓
Dashboard / Saved Plans / Files

## Screenshots

Add your project screenshots inside the `screenshots/` folder and reference them here for a presentation-ready GitHub page.

```md
![Landing Page](screenshots/landing-page.png)
![Login Page](screenshots/login-page.png)
![Dashboard](screenshots/dashboard.png)
![Diet Plan Result](screenshots/plan-result.png)
```

Recommended screenshots to include:

- landing page hero section
- login/register page
- profile form
- generated diet plan result
- cloud storage/upload workflow
- final dashboard or saved-plan view

## Folder Structure

```
AI-Powered-Personal-Diet-Planner-with-Cloud-Storage/
├── ai_engine/
│   ├── diet_engine.py
│   └── food_data.json
├── backend/
│   ├── app.py
│   ├── models/
│   ├── requirements.txt
│   ├── routes/
│   ├── services/
│   └── utils/
├── cloud/
│   ├── database_service.py
│   └── storage_service.py
├── docs/
│   ├── architecture.md
│   ├── deployment.md
│   ├── final-academic-submission.md
│   ├── project-report.md
│   ├── requirements-checklist.md
│   ├── submission-summary.md
│   ├── testing.md
│   ├── viva-script.md
│   └── interview-prep.md
├── frontend/
│   ├── package.json
│   ├── src/
│   ├── public/
│   └── vite.config.js
├── screenshots/
├── sample_data/
├── tests/
│   └── test_app.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Local Setup

### 1. Clone the project

```bash
git clone <your-repo-url>
cd AI-Powered-Personal-Diet-Planner-with-Cloud-Storage
```

### 2. Create Python environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install backend dependencies

```bash
cd backend
python -m pip install -r requirements.txt
```

### 4. Install frontend dependencies

```bash
cd ../frontend
npm install
```

### 5. Start backend

```bash
cd ../backend
python app.py
```

### 6. Start frontend

```bash
cd ../frontend
npm run dev -- --host 0.0.0.0
```

Open:

- Frontend: http://localhost:5173
- Backend: http://localhost:5000

## Backend API Endpoints

Authentication:

- POST /api/auth/register
- POST /api/auth/login
- POST /api/auth/logout
- GET /api/auth/me

Profile:

- GET /api/profile
- PUT /api/profile
- GET /api/profile/targets

Plans:

- POST /api/plans/generate
- GET /api/plans
- GET /api/plans/<plan_id>
- DELETE /api/plans/<plan_id>

Storage:

- POST /api/storage/upload
- GET /api/storage/files
- GET /api/storage/files/<file_id>/download
- DELETE /api/storage/files/<file_id>

## AI Recommendation Approach

This project uses a rule-based recommendation engine for meal generation. It evaluates:

- dietary preference
- calories and macros
- allergies
- goal type
- general health/wellness preference

It deliberately avoids medical claims and labels outputs as educational/demo wellness guidance.

## Testing

The automated backend suite is in:

- `tests/test_app.py`

Run:

```bash
python -m pytest tests/test_app.py -q
```

## Security and Data Privacy

The project follows basic security principles:

- user authentication via JWT
- user-specific data access
- input validation
- protected routes
- no credentials stored in source files
- environment variables for secrets

## Deployment Notes

This project is designed to run locally first and can be extended to cloud deployment using:

- Firebase Hosting + Authentication + Firestore + Storage
- Supabase for auth/database/storage
- Vercel + Render + Railway for frontend/backend hosting
- AWS/Azure/GCP services for advanced deployment

See the docs in the `docs/` folder for detailed deployment guidance.

## GitHub Strategy

This repo is structured to look like a real, polished student project by including:

- organized folders
- a clear README
- modular backend frontend code
- tests
- architecture and deployment notes
- a professional project narrative

## Disclaimer

This project is for educational and general wellness demonstration. Generated diet plans are not medical advice and should not replace professional nutrition or clinical guidance.

## Future Enhancements

- meal history analytics
- user dashboards with charts
- better AI API integration with fallback logic
- cloud database migration to Firebase/Supabase
- file storage to S3/Firebase Storage
- CI/CD deployment pipeline

## License

This project is for educational use.
