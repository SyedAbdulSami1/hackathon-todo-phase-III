<!-- Sync Impact Report
Version change: 1.0.0 → 1.1.0
List of modified principles: Strict Spec-Driven Development → Strict Spec-Driven Development (Preserved Phase I & II Architecture)
Added sections: AI Chatbot Isolated Feature Module, Statelessness with Persistent Storage, Vercel-Safe Deployment
Removed sections: None
Templates requiring updates:
- ✅ .specify/templates/plan-template.md
- ✅ .specify/templates/spec-template.md
- ✅ .specify/templates/tasks-template.md
- ✅ .specify/templates/commands/sp.constitution.md
Follow-up TODOs:
- TODO(RATIFICATION_DATE): Original ratification date is unknown.
-->

# Hackathon II – Evolution of Todo – Phase III AI Chatbot Integration Constitution

## Core Principles

### Strict Spec-Driven Development (Preserved Phase I & II Architecture)
Every feature implementation must start from a written specification; Specifications must be clear, testable, and cover all acceptance criteria; Manual coding without a spec is prohibited; All Phase I & II architecture and functionality must remain unchanged during Phase III development.

### Monorepo Architecture
The project will use a monorepo structure with frontend (Next.js 14 App Router) and backend (Python FastAPI) components.

### Secure JWT Authentication (Unchanged)
All API interactions will be secured using JWT authentication. Backend FastAPI will verify JWTs, and frontend will manage token storage and transmission. Better Auth will be used for token issuance. JWT authentication mechanisms must remain unchanged during Phase III.

### Strict User Data Isolation
Each user's data must be strictly isolated. All database queries and API responses must be filtered by the authenticated user's ID.

### Clean, Testable, Type-Safe Code
Code must be clean, maintainable, and type-safe. Use SQLModel for backend ORM, and TypeScript for frontend. All code should be easily testable.

### AI Chatbot Isolated Feature Module
The AI Chatbot feature must be implemented as an isolated module with minimal coupling to existing codebase. No breaking changes to existing architecture, APIs, or database schemas are allowed. The chatbot functionality should be contained in dedicated modules/files separate from existing task management functionality.

### No Breaking Database Changes (Additive Only)
Database schema changes must be additive only. No existing tables, columns, or relationships may be modified or deleted. New tables and columns are permitted but must not interfere with existing functionality. Migrations must be backward-compatible.

### Statelessness with Persistent Storage
Backend services must remain stateless, with all persistent state stored in Neon PostgreSQL database. No in-memory state storage or session persistence on the server-side. All chatbot conversation history and user preferences must be stored in the database.

### Vercel-Safe Deployment
All code changes must be compatible with Vercel deployment platform. No server-specific functionality or file system dependencies that would break Vercel deployment. Environment variables and build configurations must work seamlessly with Vercel's deployment pipeline.

## Key Standards

All API endpoints must require a valid JWT. Every task and data record must be filtered by the authenticated `user_id`. Use SQLModel with Neon PostgreSQL for the database. The frontend will use Next.js App Router with Server Components as the default. Tailwind CSS will be used for all styling. AI Chatbot features must integrate seamlessly with existing authentication and data isolation patterns.

## Constraints

No new technologies outside the specified stack. The application must support multiple users from day one. CORS must be properly configured for inter-service communication. No breaking changes to existing API endpoints. Database schema changes must be additive only. Server statelessness must be maintained.

## Development Workflow

Amendments to this constitution require a documented proposal, a review of impact on dependent artifacts, and approval by the project lead. Versioning follows Semantic Versioning rules (MAJOR.MINOR.PATCH). Compliance will be reviewed during integration testing phases. All changes must preserve Phase I & II functionality while adding AI Chatbot features in isolation.

**Version**: 1.1.0 | **Ratified**: TODO(RATIFICATION_DATE): Original ratification date is unknown. | **Last Amended**: 2026-02-22