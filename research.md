# Research Findings: AI Chatbot Implementation

## MCP Tool Schemas

### Decision: MCP Tool Schemas
**Rationale**: Identified 5 essential MCP tools for todo management functionality that align with the architecture requirements and user stories from the specification.

**Alternatives considered**: More complex tools vs simpler tools vs direct API integration

**Final Selection**:
- **todo_create_tool**: Create new todo tasks
  - Input: {title: string, description?: string, due_date?: string, priority?: string}
  - Output: {success: boolean, task_id: string, message: string}

- **todo_update_tool**: Update existing todo tasks
  - Input: {task_id: string, title?: string, description?: string, due_date?: string, status?: string, priority?: string}
  - Output: {success: boolean, message: string}

- **todo_delete_tool**: Delete todo tasks
  - Input: {task_id: string} or {title: string}
  - Output: {success: boolean, message: string}

- **todo_search_tool**: Search/list existing tasks
  - Input: {status?: string, priority?: string, search_term?: string, limit?: number}
  - Output: {tasks: Array<{id, title, status, priority, due_date}>}

- **todo_complete_tool**: Mark tasks as complete/incomplete
  - Input: {task_id: string, complete: boolean}
  - Output: {success: boolean, message: string}

## Stateless Execution Sequence

### Decision: Stateless Execution Sequence
**Rationale**: Designed 8-step flow that maintains statelessness while preserving conversation context and aligning with the architecture requirements.

**Alternatives considered**: Different step breakdowns and execution patterns

**Final 8-Step Flow**:
1. **Authenticate**: Validate JWT token and confirm user_id matches
2. **Validate Input**: Parse and validate user input message
3. **Load Context**: Retrieve conversation history from DB if provided
4. **Process Intent**: Use AI to identify user intent and extract parameters
5. **Map to Tool**: Select appropriate MCP tool based on identified intent
6. **Execute Tool**: Run selected MCP tool with extracted parameters
7. **Store Message**: Persist conversation and message in DB
8. **Return Response**: Send AI-generated response back to user

## Vercel Environment Variables

### Decision: Vercel Environment Variables
**Rationale**: Identified essential environment variables needed for Vercel deployment while maintaining security and configuration best practices.

**Alternatives considered**: Different configuration approaches

**Required Variables**:
- `DATABASE_URL`: Database connection string for Neon PostgreSQL
- `JWT_SECRET`: Secret for JWT verification (same as existing system)
- `MCP_TOOL_CONFIG`: JSON configuration for MCP tools (optional)
- `OPENAI_API_KEY`: API key for AI services (if using OpenAI)
- `ANTHROPIC_API_KEY`: API key for AI services (if using Anthropic)
- `NEXT_PUBLIC_CHAT_ENABLED`: Flag to enable/disable chat UI

## Agent Initialization Pattern

### Decision: Agent Initialization Pattern
**Rationale**: Chose application-lifecycle-based initialization for optimal performance and resource management while maintaining statelessness.

**Alternatives considered**: Request-scoped vs global singleton vs dependency injection

**Implementation**:
- Initialize agent instance on application startup in FastAPI lifespan event
- Store agent instance in application state for reuse
- Properly dispose of resources on application shutdown
- Use dependency injection to access agent instance in route handlers