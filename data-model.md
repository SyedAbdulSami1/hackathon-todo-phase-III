# Data Model: AI Chatbot for Natural Language Todo Management

## Entities

### Conversation Entity
Represents a single chat session between a user and the AI assistant, containing metadata about the conversation context and user association.

**Fields**:
- `id` (UUID, Primary Key): Unique identifier for the conversation
- `user_id` (String, Required, Indexed): Foreign key to user for data isolation
- `title` (String, Optional, Max 200 chars): Auto-generated or user-provided conversation title
- `created_at` (DateTime, Required): Timestamp when conversation was initiated
- `updated_at` (DateTime, Required): Timestamp of last activity in conversation
- `metadata` (JSON, Optional): Additional context data for the conversation

**Constraints**:
- `user_id` must reference a valid user in the system
- `created_at` defaults to current timestamp
- `updated_at` updates automatically on any changes
- Index on `user_id` for efficient user-specific queries

**Relationships**:
- One Conversation to Many Messages (one-to-many)

### Message Entity
Represents individual exchanges within a conversation, storing the user input, AI response, and any associated action taken.

**Fields**:
- `id` (UUID, Primary Key): Unique identifier for the message
- `conversation_id` (UUID, Required, Indexed): Foreign key to Conversation
- `sender_type` (Enum, Required): Values: ['user', 'assistant', 'system']
- `content` (Text, Required): The actual message content
- `timestamp` (DateTime, Required): When the message was created
- `tool_used` (String, Optional): Name of MCP tool used in response
- `tool_parameters` (JSON, Optional): Parameters passed to the MCP tool
- `tool_result` (JSON, Optional): Result returned by the MCP tool
- `message_type` (Enum, Optional): Values: ['text', 'tool_call', 'tool_response']

**Constraints**:
- `conversation_id` must reference a valid conversation
- `sender_type` must be one of the allowed enum values
- `timestamp` defaults to current timestamp
- Index on `conversation_id` for efficient conversation queries

**Relationships**:
- Many Messages to One Conversation (many-to-one)

## Validation Rules

### Conversation Validation
- User ID must match authenticated user (enforced by application logic)
- Title length limited to 200 characters
- Cannot create conversation for non-existent user

### Message Validation
- Content cannot be empty
- Sender type must be valid enum value
- Message must belong to an existing conversation
- Tool parameters and results must be valid JSON when present

## State Transitions

### Conversation States
- Active: Currently ongoing conversation
- Archived: Conversation completed after period of inactivity
- Deleted: Conversation marked for deletion (soft delete)

### Message States
- Pending: Message received but not yet processed
- Processed: Message processed and response generated
- Failed: Message processing failed (for error tracking)

## Indexes for Performance

### Required Indexes
- Conversation: Index on (user_id, updated_at) for efficient user conversation retrieval
- Message: Index on (conversation_id, timestamp) for chronological message retrieval
- Message: Index on (sender_type) for filtering by sender

### Optional Indexes
- Conversation: Index on (user_id, created_at) for historical conversation retrieval
- Message: Index on (tool_used) for tool usage analytics