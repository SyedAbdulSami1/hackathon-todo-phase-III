"""Unit tests for the AI Chatbot agents."""

import pytest
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from agents.config import AgentConfig
from agents.chat_agent import ChatAgent
from agents.tool_binder import ToolBinder
from agents.factory import AgentFactory


def test_agent_config_initialization():
    """Test AgentConfig initialization with default values."""
    with patch.dict('os.environ', {}, clear=True):
        config = AgentConfig()
        assert config.model_name == "gpt-4"
        assert config.temperature == 0.7
        assert config.max_tokens == 1000


def test_agent_config_to_dict():
    """Test AgentConfig to_dict method."""
    config = AgentConfig()
    config_dict = config.to_dict()
    assert config_dict["model_name"] == config.model_name
    assert config_dict["temperature"] == config.temperature


@patch('agents.chat_agent.AsyncOpenAI')
def test_chat_agent_initialization(mock_openai):
    """Test ChatAgent initialization."""
    config = AgentConfig()
    agent = ChatAgent(config)
    
    assert agent.config == config
    assert agent.model_name in ["gemini-1.5-flash", "gemini-flash-latest", config.model_name]
    mock_openai.assert_called_once()


@pytest.mark.asyncio
@patch('agents.chat_agent.AsyncOpenAI')
async def test_chat_agent_process_request_basic(mock_openai_class):
    """Test ChatAgent process_request basic interaction."""
    mock_client = MagicMock()
    mock_openai_class.return_value = mock_client
    
    # Mock response from OpenAI
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    mock_message.content = "Hello there!"
    mock_message.tool_calls = None
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    
    # completions.create is async
    mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
    
    agent = ChatAgent()
    result = await agent.process_request("Hi")
    
    assert result["response"] == "Hello there!"
    assert result["tool_calls"] == []
    assert "General interaction" in result["actions_taken"]


@pytest.mark.asyncio
@patch('agents.chat_agent.AsyncOpenAI')
async def test_chat_agent_process_request_with_tools(mock_openai_class):
    """Test ChatAgent process_request with tool calls."""
    mock_client = MagicMock()
    mock_openai_class.return_value = mock_client
    
    # First response: call a tool
    mock_tool_call = MagicMock()
    mock_tool_call.id = "call_123"
    mock_tool_call.function.name = "add_task"
    mock_tool_call.function.arguments = '{"title": "Buy milk"}'
    
    mock_response1 = MagicMock()
    mock_message1 = MagicMock()
    mock_message1.content = None
    mock_message1.tool_calls = [mock_tool_call]
    mock_response1.choices = [MagicMock(message=mock_message1)]
    
    # Second response: final friendly text
    mock_response2 = MagicMock()
    mock_message2 = MagicMock()
    mock_message2.content = "I've added the task for you."
    mock_message2.tool_calls = None
    mock_response2.choices = [MagicMock(message=mock_message2)]
    
    mock_client.chat.completions.create = AsyncMock(side_effect=[mock_response1, mock_response2])
    
    # Mock tool registry
    mock_registry = MagicMock()
    mock_registry.execute_tool = AsyncMock(return_value={"success": True, "task_id": 1})
    
    agent = ChatAgent()
    agent.tools = mock_registry
    
    result = await agent.process_request("Add buy milk task")
    
    assert result["response"] == "I've added the task for you."
    assert len(result["tool_calls"]) == 1
    assert result["tool_calls"][0]["name"] == "add_task"
    assert "Action: add_task" in result["actions_taken"]


def test_tool_binder_initialization():
    """Test ToolBinder initialization."""
    agent = MagicMock()
    binder = ToolBinder(agent)
    assert binder.agent == agent
    assert binder.tool_registry is not None


def test_agent_factory_create_chat_agent():
    """Test AgentFactory create_chat_agent method."""
    with patch('agents.chat_agent.AsyncOpenAI'):
        agent = AgentFactory.create_chat_agent()
        assert isinstance(agent, ChatAgent)


def test_agent_factory_create_default_agent():
    """Test AgentFactory create_default_agent method."""
    with patch('agents.chat_agent.AsyncOpenAI'):
        agent = AgentFactory.create_default_agent()
        assert isinstance(agent, ChatAgent)
