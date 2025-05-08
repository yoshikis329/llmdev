class Authenticator:
    def __init__(self):
        self.users = {} # ユーザ情報を格納（インスタンス変数）
    
    # ユーザの登録
    def register(self, username, password):
        if username in self.users:
            raise ValueError("エラー: ユーザは既に存在します。")
        else:
            self.users[username] = password

    # ログイン
    def login(self, username, password):
        if self.users.get(username) == password:
            return "ログイン成功"
        else:
            raise ValueError("エラー: ユーザ名またはパスワードが正しくありません。")