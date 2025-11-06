from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool
import os
import tiktoken

# インデックスデータベースを作成する関数
def store_database(embedding_model, persist_directory, chat_ai_model_name):
    # 実行中のスクリプトのパスを取得
    current_script_path = os.path.abspath(__file__)

    # 実行中のスクリプトが存在するディレクトリを取得
    current_directory = os.path.dirname(current_script_path)
    # PDFファイルを読込
    loader = DirectoryLoader(f'{current_directory}/data/pdf', glob="**/*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()

    # チャンクに分割
    encoding_name = tiktoken.encoding_for_model(chat_ai_model_name).name
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(encoding_name)
    texts = text_splitter.split_documents(documents)

    # データベースに保存
    db = Chroma.from_documents(texts, embedding_model, persist_directory=persist_directory)
    return db


# dbツールの作成
def create_db_tool(chat_ai_model_name):
    # 実行中のスクリプトのパスを取得
    current_script_path = os.path.abspath(__file__)
    # 実行中のスクリプトが存在するディレクトリを取得
    current_directory = os.path.dirname(current_script_path)

    # インデックスの保存先
    persist_directory = f'{current_directory}/chroma_db'

    # エンベディングモデル
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

    if os.path.exists(persist_directory):
        try:
            # 既存のデータベースを読み込む
            db = Chroma(persist_directory=persist_directory, embedding_function=embedding_model)
        except Exception as e:
            print(f"読み込めませんでした。エラー：{e}")
            db = store_database(embedding_model, persist_directory, chat_ai_model_name)
    else:
        # 新しいデータベースを作成
        db = store_database(embedding_model, persist_directory, chat_ai_model_name)

    retriever = db.as_retriever()
    return create_retriever_tool(retriever, "retriever_health_information", "Search for health information in the database")