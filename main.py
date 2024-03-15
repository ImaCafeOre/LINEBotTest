import requests
from flask import Flask, request, abort
from linebot import (
LineBotApi, WebhookHandler
)
from linebot.exceptions import (
InvalidSignatureError
)
from linebot.models import (
MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

# アプリの冒頭でユーザーごとに最後に参照したURLを保存する辞書を初期化
user_last_url = {}

# LINE Messaging API の準備
line_bot_api = LineBotApi('チャネルアクセストークンを入力')
handler = WebhookHandler('チャネルシークレットを入力')

# 外部システムに質問を送信し、回答を取得する関数
def get_answer_from_external_system(urls,question):
    url = urls # "https://tak-campus-guide-xrbc.onrender.com/"
    params = {'query': question}
    response = requests.get(url, params=params)
    response_json = response.json()
    return response_json['answer']

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # メッセージを小文字に変換して処理
    user_id = event.source.user_id
    text_message = event.message.text.lower()

        if urls is None:
            # 直前に記憶したURLがない場合、質問の促しを返信
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="こんにちは。動作しています。"))
            return  # ここで処理を終了して、以降の処理をスキップ


    # ユーザーごとに最後に参照したURLを更新
    user_last_url[user_id] = urls

    # 外部システムに質問を送り、回答を取得
    answer = get_answer_from_external_system(urls, event.message.text)
    # LINE に回答を返信
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=answer))

if __name__ == "__main__":
    app.run()
