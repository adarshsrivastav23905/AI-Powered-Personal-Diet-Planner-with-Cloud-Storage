# Cloud Deployment Guide

## Local Development

Use the local app first before any cloud deployment:

```bash
cd backend
python app.py
```

Then run the frontend:

```bash
cd frontend
npm run dev -- --host 0.0.0.0
```

## Free or Beginner-Friendly Cloud Options

### Option 1: Firebase

- Frontend: Firebase Hosting
- Backend: Cloud Functions or a lightweight backend deployment
- Database: Firestore
- Storage: Firebase Storage
- Auth: Firebase Authentication

### Option 2: Supabase

- Auth: Supabase Auth
- Database: Postgres database
- Storage: Supabase Storage
- Frontend: Vercel or Netlify

### Option 3: Render / Railway + Vercel

- Frontend: Vercel
- Backend: Render or Railway
- Database: SQLite for demo or managed Postgres for production

## Production Deployment Checklist

- move secrets to environment variables
- disable debug mode
- enable HTTPS only
- restrict database access
- validate uploads
- add logging and monitoring
- use secure JWT secret
- keep AI fallback logic active

## Deployment Guidance

This project is intentionally structured so the local version works without paid cloud services. That makes it easier for students to learn, test, and document the architecture before moving to a real cloud platform.
