import getpass
import os
import uuid
from dataclasses import dataclass, field
from typing import Annotated, List

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, AnyMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.graph.ui import push_ui_message
from langgraph.managed import IsLastStep


@dataclass
class InputState:
    messages: Annotated[List[AnyMessage], add_messages] = field(default_factory=list)


@dataclass
class State(InputState):
    is_last_step: IsLastStep = field(default=False)


def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")


load_dotenv()
_set_env("OPENAI_API_KEY")


graph_builder = StateGraph(State)


llm = init_chat_model("openai:gpt-4.1-mini")


def chatbot(state: State):
    super_gnar = AIMessage(
        id=str(uuid.uuid4()),
        content="""I got a push example for you, this will help explain to the user what's going on.""",
    )

    my_data_to_push = {...}
    push_ui_message("writer", my_data_to_push, message=super_gnar)

    return {"messages": [llm.invoke(state.messages)]}


# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()
graph = graph_builder.compile()
