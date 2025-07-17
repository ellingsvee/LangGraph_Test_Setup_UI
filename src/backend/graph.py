import getpass
import os
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Annotated, List

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, AnyMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.graph.ui import AnyUIMessage, push_ui_message, ui_message_reducer
from langgraph.managed import IsLastStep


@dataclass
class InputState:
    messages: Annotated[List[AnyMessage], add_messages] = field(default_factory=list)
    ui: Annotated[List[AnyUIMessage], ui_message_reducer] = field(default_factory=list)


@dataclass
class State(InputState):
    is_last_step: IsLastStep = field(default=False)


def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")


load_dotenv()
_set_env("OPENAI_API_KEY")


def simple_agent(state: State):
    """Simple agent that responds to user messages and displays a UI."""
    model = init_chat_model("openai:gpt-4.1-mini")

    # Filter for human messages to get user input
    user_messages = [m for m in state.messages if m.type == "human"]

    print("All messages:", [(m.type, m.content) for m in state.messages])
    print("User messages:", [(m.type, m.content) for m in user_messages])
    print("Last user message:", user_messages[-1] if user_messages else None)

    # Create system message and pass conversation to model
    system_message = {
        "type": "system",
        "content": "You are a helpful assistant. Provide brief, friendly responses. Keep it to 1-2 sentences.",
    }

    # Prepare messages for the model
    messages_for_model = [system_message] + state.messages

    # Get LLM response
    llm_response = model.invoke(messages_for_model)
    content = llm_response.content

    # Generate timestamp
    timestamp = datetime.now().strftime("%H:%M:%S")

    # Push UI message
    ui_data = {
        "message": content,
        "title": "AI Assistant",
        "timestamp": timestamp,
    }

    print("Pushing UI message:", ui_data)

    # Create a simple AI message first
    ai_message = AIMessage(
        id=str(uuid.uuid4()),
        content=content,
    )

    # Push the UI message
    push_ui_message("simple-ui", ui_data, message=ai_message)

    return {"messages": [ai_message]}


# Create the graph
graph_builder = StateGraph(State)
graph_builder.add_node("simple-agent", simple_agent)
graph_builder.add_edge(START, "simple-agent")
graph_builder.add_edge("simple-agent", END)

graph = graph_builder.compile()
graph.name = "Simple UI Demo"
