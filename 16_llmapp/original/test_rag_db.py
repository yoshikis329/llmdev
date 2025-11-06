import pytest
import os
from dotenv import load_dotenv
from original.rag_db import store_database, create_db_tool
from langchain_openai import OpenAIEmbeddings

@pytest.fixture(autouse=True)
def setup_environment():
    """
    テスト実行前に環境変数を設定する
    """
    load_dotenv(".env")
    os.environ["OPENAI_API_KEY"] = os.environ["API_KEY"]
    yield

def test_store_database():
    """
    データベースが正しく保存されるかをテスト。
    """

    # モデル名と保存ディレクトリの設定
    chat_ai_model_name = "gpt-4o-mini"
    persist_directory = "./test_chroma_db"
    
    # エンベディングモデルの作成
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
    
    # データベースの保存
    db = store_database(embedding_model, persist_directory, chat_ai_model_name)
    
    assert db is not None, "データベースが正常に保存されていません。"

def test_create_db_tool_success():
    """
    RAGツールが正しく作成されるかをテスト。
    """
    chat_ai_model_name = "gpt-4o-mini"
    
    # RAGツールの作成
    db_tool = create_db_tool(chat_ai_model_name)
    
    assert db_tool is not None, "RAGツールが正常に作成されていません。"
    assert db_tool.name == "retriever_health_information", "RAGツールの名前が正しくありません。"
    assert db_tool.description == "Search for health information in the database", "RAGツールの説明が正しくありません。"
    assert callable(db_tool.func), "RAGツールの関数が呼び出し可能である必要があります。"

def test_create_db_tool_init():
    """
    RAGツールの初期化が正しく行われるかをテスト。
    """
    chat_ai_model_name = "gpt-4o-mini"

    try: 
        # カレントディレクトリの変更
        os.mkdir("test_rag_db")
        os.chdir("test_rag_db")
    
        # RAGツールの作成
        db_tool = create_db_tool(chat_ai_model_name)
    
        # ツールの初期化を確認
        assert db_tool is not None, "RAGツールが正常に作成されていません。"
        assert db_tool.name == "retriever_health_information", "RAGツールの名前が正しくありません。"
        assert db_tool.description == "Search for health information in the database", "RAGツールの説明が正しくありません。"
        assert callable(db_tool.func), "RAGツールの関数が呼び出し可能である必要があります。"
    
    finally:
        # 後処理
        os.chdir("..")
        os.removedirs("test_rag_db")