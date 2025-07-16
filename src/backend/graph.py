from typing import Annotated
import uuid

from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langgraph.graph.ui import push_ui_message
from langchain_core.messages import AIMessage


class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)


llm = init_chat_model("openai:gpt-4.1-mini")


async def chatbot(state: State):

    super_gnar = AIMessage(
                id=str(uuid.uuid4()),
                content=f"""I got a push example for you, this will help explain to the user what's going on."""
    )

    my_data_to_push = {...}

    push_ui_message("writer", my_data_to_push, message=super_gnar)

    return {"messages": [llm.invoke(state["messages"])]}


# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()