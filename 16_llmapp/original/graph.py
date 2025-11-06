from langchain_community.tools.tavily_search import TavilySearchResults
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from original.rag_db import create_db_tool


# ツール定義
def create_tools(chat_ai_model_name):
    search_tool = TavilySearchResults(max_results=3)
    rag_tool = create_db_tool(chat_ai_model_name)
    return [search_tool, rag_tool]


# Stateクラスの作成
class State(TypedDict):
    messages: Annotated[list, add_messages]


# グラフ構築
def build_graph(chat_ai_model_name, memory):
    # ツールの追加
    graph_builder = StateGraph(State)
    tools = create_tools(chat_ai_model_name)
    tool_node = ToolNode(tools)
    graph_builder.add_node(tool_node, "tools")

    # チャットの追加
    llm = ChatOpenAI(model_name=chat_ai_model_name)
    llm_with_tools = llm.bind_tools(tools)
    def chatbot(state: State):
        return {"messages": [llm_with_tools.invoke(state["messages"])]}
    graph_builder.add_node(chatbot, "chatbot")

    # スタートノードの設定
    graph_builder.set_entry_point("chatbot")
    graph_builder.add_conditional_edges(
        "chatbot",
        tools_condition
    )
    graph_builder.add_edge("tools", "chatbot")

    return graph_builder.compile(checkpointer=memory)


# グラフを実行する関数
def execute_graph(graph: StateGraph, user_message: str, role: str):
    response = graph.invoke(
        {"messages": [("user", user_message), ("system", role)]},
        {"configurable": {"thread_id": "1"}},
        stream_mode="values",
    )
    return response["messages"][-1].content