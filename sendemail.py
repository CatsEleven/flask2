import requests
import json

def send_email(url, address, subject, content):
    """
    指定されたアドレスにメールを送信する。

    Args:
        url (str): WebアプリケーションのURL
        address (str): 受信者のメールアドレス
        subject (str): メールの件名
        content (int): メールの内容（1：正常、その他：異常）

    Returns:
        str: Webアプリケーションからのレスポンス
    """
    # リクエストボディ
    data = {
        'address': address,
        'subject': subject,
        'content': content
    }

    # リクエストヘッダー
    headers = {
        'Content-Type': 'application/json'
    }

    # POSTリクエスト送信
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # レスポンスの返却
    return response.text
