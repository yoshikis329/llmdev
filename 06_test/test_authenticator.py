from authenticator import Authenticator
import pytest

def test_register():
    authenticator = Authenticator()
    authenticator.register("test_user", "password123")
    assert authenticator.users["test_user"] == "password123"

def test_register_existing_user():
    authenticator = Authenticator()
    authenticator.register("test_user", "password123")    
    with pytest.raises(ValueError, match="エラー: ユーザは既に存在します。"):
        authenticator.register("test_user", "new_password")

def test_login_success():
    authenticator = Authenticator()
    authenticator.register("test_user", "password123")
    assert authenticator.login("test_user", "password123") == "ログイン成功"

def test_login_fail():
    authenticator = Authenticator()
    authenticator.register("test_user", "password123")
    with pytest.raises(ValueError, match="エラー: ユーザ名またはパスワードが正しくありません。"):
        authenticator.login("test_user", "password456")