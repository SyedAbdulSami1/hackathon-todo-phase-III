# AI-Powered Todo Chatbot (Hackathon Phase III)

A premium, startup-quality Todo application featuring an AI Chatbot powered by Google Gemini and MCP (Model Context Protocol) for task management.

## 🚀 Recent Updates & Fixes
- **✅ Fixed 500 Errors:** Resolved a critical bug where a folder named `logging` shadowed the standard library. Renamed to `internal_logging`.
- **✅ Backend Entrypoint:** Unified entrypoint to `index.py` with path-adjustment logic for Vercel/Local compatibility.
- **✅ Neon DB Optimization:** Added SSL support (`sslmode=require`) for secure database connections.
- **✅ Premium UI/UX:** Enhanced the Chatbot with high-end animations, glassmorphism, and interactive "AI is thinking" states.
- **✅ Verified Tests:** All 66 backend tests (unit & integration) are passing.

## 🛠️ Local Setup

### 1. Backend (FastAPI)
```bash
cd backend
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file with your keys
# GOOGLE_API_KEY=your_key
# DATABASE_URL=your_postgres_url

# Run the server
uvicorn index:app --reload --port 8000
```

### 2. Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev
```
Access the app at `http://localhost:3000`.

## 🧪 Testing Report
**Status:** 🟢 PASSING (All 66 Tests)
**Date:** February 28, 2026

| Test Suite | Result | Count |
|------------|--------|-------|
| Integration (Endpoints) | ✅ PASS | 9 |
| Main App Lifecycle | ✅ PASS | 9 |
| AI Agents | ✅ PASS | 8 |
| Exceptions | ✅ PASS | 14 |
| MCP Tools | ✅ PASS | 8 |
| Data Models | ✅ PASS | 5 |
| Services | ✅ PASS | 13 |
| **Total** | **✅ PASS** | **66** |

Full report available in `backend/pytest-result.txt`.

## 📂 Project Structure
- `frontend/`: Next.js application with Tailwind CSS.
- `backend/`: FastAPI application with SQLModel.
- `backend/agents/`: AI logic and Gemini integration.
- `backend/tools/`: MCP tool implementations.
- `backend/internal_logging/`: Custom logging (renamed from 'logging' to avoid conflicts).
