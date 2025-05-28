# メモリの設定
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from graph import build_graph, execute_graph


# 環境変数を取り込む
load_dotenv(".env")
os.environ["OPENAI_API_KEY"] = os.environ["API_KEY"]


# 使用するモデル名
MODEL_NAME = "gpt-4o-mini"


# メイン関数
def main():
    memory = MemorySaver()

    role = ""
    while not role:
       role = input("あなたの役割を入力してください (例: あなたは猫です。):")

    # グラフの構築
    graph = build_graph(MODEL_NAME, memory)

    while True:
        # ユーザーメッセージの入力
        user_message = input("質問: ")
        if user_message == "":
            print("終了します。")
            break
    
        print(user_message)
        # グラフの実行
        response = execute_graph(graph, user_message, role)

        # レスポンスの表示
        print("返答:", response)


if __name__ == "__main__":
    main()