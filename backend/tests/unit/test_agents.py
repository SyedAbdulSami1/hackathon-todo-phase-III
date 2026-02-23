"""Unit tests for the AI Chatbot agents."""

import pytest
from agents.config import AgentConfig
from agents.chat_agent import ChatAgent
from agents.tool_binder import ToolBinder
from agents.factory import AgentFactory


def test_agent_config_initialization():
    """Test AgentConfig initialization with default values."""
    config = AgentConfig()

    assert config.model_name == "gpt-4"
    assert config.temperature == 0.7
    assert config.max_tokens == 1000
    assert config.provider == "openai"
    assert config.enable_mcp_tools is True
    assert config.tool_execution_timeout == 30


def test_agent_config_from_env(mocker):
    """Test AgentConfig initialization with environment variables."""
    mocker.patch.dict('os.environ', {
        'AGENT_MODEL_NAME': 'gpt-3.5-turbo',
        'AGENT_TEMPERATURE': '0.5',
        'AGENT_MAX_TOKENS': '500',
        'AGENT_PROVIDER': 'anthropic',
        'ENABLE_MCP_TOOLS': 'false',
        'TOOL_EXECUTION_TIMEOUT': '60'
    })

    config = AgentConfig()

    assert config.model_name == 'gpt-3.5-turbo'
    assert config.temperature == 0.5
    assert config.max_tokens == 500
    assert config.provider == 'anthropic'
    assert config.enable_mcp_tools is False
    assert config.tool_execution_timeout == 60


def test_agent_config_to_dict():
    """Test AgentConfig to_dict method."""
    config = AgentConfig()
    config_dict = config.to_dict()

    assert 'model_name' in config_dict
    assert 'temperature' in config_dict
    assert 'max_tokens' in config_dict
    assert 'provider' in config_dict
    assert config_dict['model_name'] == config.model_name


def test_chat_agent_initialization():
    """Test ChatAgent initialization."""
    agent = ChatAgent()

    assert agent.config is not None
    assert agent.tools is not None


def test_chat_agent_process_request_general():
    """Test ChatAgent process_request with general input."""
    agent = ChatAgent()

    result = agent.process_request("Hello, how are you?")

    assert 'response' in result
    assert 'tool_used' in result
    assert 'actions_taken' in result
    assert isinstance(result['actions_taken'], list)


def test_chat_agent_parse_intent_create():
    """Test ChatAgent _parse_intent for create actions."""
    agent = ChatAgent()

    intent = agent._parse_intent("Create a task to buy milk")

    assert intent['needs_tool'] is True
    assert intent['tool_name'] == 'todo_create_tool'


def test_chat_agent_parse_intent_update():
    """Test ChatAgent _parse_intent for update actions."""
    agent = ChatAgent()

    intent = agent._parse_intent("Update task 1 to be more important")

    assert intent['needs_tool'] is True
    assert intent['tool_name'] == 'todo_update_tool'


def test_chat_agent_parse_intent_delete():
    """Test ChatAgent _parse_intent for delete actions."""
    agent = ChatAgent()

    intent = agent._parse_intent("Delete the old task")

    assert intent['needs_tool'] is True
    assert intent['tool_name'] == 'todo_delete_tool'


def test_chat_agent_parse_intent_search():
    """Test ChatAgent _parse_intent for search actions."""
    agent = ChatAgent()

    intent = agent._parse_intent("Show me all my tasks")

    assert intent['needs_tool'] is True
    assert intent['tool_name'] == 'todo_search_tool'


def test_chat_agent_parse_intent_complete():
    """Test ChatAgent _parse_intent for complete actions."""
    agent = ChatAgent()

    intent = agent._parse_intent("Mark task 1 as complete")

    assert intent['needs_tool'] is True
    assert intent['tool_name'] == 'todo_complete_tool'


def test_chat_agent_parse_intent_general():
    """Test ChatAgent _parse_intent for general input."""
    agent = ChatAgent()

    intent = agent._parse_intent("Just saying hi")

    assert intent['needs_tool'] is False


def test_chat_agent_extract_title():
    """Test ChatAgent _extract_title method."""
    agent = ChatAgent()

    title = agent._extract_title("Create a task to buy milk and bread")

    assert title is not None
    assert "buy milk" in title.lower() or "milk and bread" in title.lower()


def test_chat_agent_extract_task_id():
    """Test ChatAgent _extract_task_id method."""
    agent = ChatAgent()

    task_id = agent._extract_task_id("Update task 123 to be more important")

    assert task_id == 123


def test_chat_agent_get_available_tools():
    """Test ChatAgent get_available_tools method."""
    agent = ChatAgent()

    tools_info = agent.get_available_tools()

    assert isinstance(tools_info, list)
    assert len(tools_info) > 0  # Should have at least one tool


def test_tool_binder_initialization():
    """Test ToolBinder initialization."""
    agent = ChatAgent()
    binder = ToolBinder(agent)

    assert binder.agent == agent
    assert binder.tool_registry is not None


def test_tool_binder_bind_tools():
    """Test ToolBinder bind_tools_to_agent method."""
    agent = ChatAgent()
    binder = ToolBinder(agent)

    # This should not raise an exception
    binder.bind_tools_to_agent()


def test_tool_binder_get_bound_tools_info():
    """Test ToolBinder get_bound_tools_info method."""
    agent = ChatAgent()
    binder = ToolBinder(agent)

    tools_info = binder.get_bound_tools_info()

    assert 'tool_count' in tools_info
    assert 'tools' in tools_info
    assert tools_info['tool_count'] >= 0


def test_agent_factory_create_chat_agent():
    """Test AgentFactory create_chat_agent method."""
    agent = AgentFactory.create_chat_agent()

    assert isinstance(agent, ChatAgent)


def test_agent_factory_create_default_agent():
    """Test AgentFactory create_default_agent method."""
    agent = AgentFactory.create_default_agent()

    assert isinstance(agent, ChatAgent)


def test_agent_factory_get_agent_config():
    """Test AgentFactory get_agent_config method."""
    config = AgentFactory.get_agent_config()

    assert isinstance(config, AgentConfig)
