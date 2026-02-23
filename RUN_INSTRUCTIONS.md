# How to Run Phase 3: AI Chatbot

## Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL (Neon DB or local)

## Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment (if not already done):**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Mac/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Ensure `.env` file exists in `backend/` with:
   ```
   DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
   SECRET_KEY=your_secret_key
   ```

5. **Initialize Database (Run once):**
   This step creates the required tables (including new Chat tables).
   ```bash
   # Important: Set PYTHONPATH to current directory
   # Windows (PowerShell):
   $env:PYTHONPATH='.'
   python -c "from dotenv import load_dotenv; load_dotenv(); from db import create_db_and_tables; create_db_and_tables()"
   ```

6. **Start Backend Server:**
   ```bash
   uvicorn main:app --reload
   ```
   Server will run at `http://localhost:8000`.

## Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Environment Variables:**
   Ensure `.env.local` exists in `frontend/` with:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. **Start Frontend:**
   ```bash
   npm run dev
   ```
   App will run at `http://localhost:3000`.

## Features
- **AI Chat:** Navigate to `/chat` after logging in to talk to the AI assistant about your tasks.
- **Commands:** Try "Create a task to buy milk", "List my tasks", "Complete task 1".
