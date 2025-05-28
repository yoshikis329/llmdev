import os
import pytest
from dotenv import load_dotenv
from original.graph import create_tools, build_graph
from langgraph.checkpoint.memory import MemorySaver

MODEL_NAME = "gpt-4o-mini"

@pytest.fixture(autouse=True)
def setup_environment():
    """
    テスト実行前に環境変数を設定する
    """
    load_dotenv(".env")
    os.environ["OPENAI_API_KEY"] = os.environ["API_KEY"]
    yield


def test_create_tools():
    """
    ツールが正常に作成できること
    """
    tools = create_tools(MODEL_NAME)
    assert len(tools) == 2, "ツールの数が正しくありません"
    assert tools[0].name == "tavily_search_results_json", "Tavily Searchツールが正しく作成されていません"
    assert tools[1].name == "retriever_health_information", "RAGツールが正しく作成されていません"

def test_build_graph():
    """
    グラフが正常に構築されること
    """

    memory = MemorySaver()
    graph = build_graph(MODEL_NAME, memory)

    assert graph is not None, "グラフが正常に構築されていません"
    assert "chatbot" in graph.nodes, "チャットノードがグラフに存在しません"
    assert "tools" in graph.nodes, "ツールノードがグラフに存在しません"

def test_execute_graph():
    """
    グラフが正常に実行され、応答を生成できること
    """
    memory = MemorySaver()
    graph = build_graph(MODEL_NAME, memory)

    response = graph.invoke(
        {"messages": [("user", "1たす2は何ですか？")]},
        {"configurable": {"thread_id": "1"}},
        stream_mode="values"
    )

    assert response["messages"][-1].content, "グラフが有効な応答を生成する必要があります。"
    assert "3" in response["messages"][-1].content, "計算結果が正しく応答されていません。"