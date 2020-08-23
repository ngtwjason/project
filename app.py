import os
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


line_bot_api = LineBotApi('VUk50GBnI4Zif8HoFzzALsZ6cAYRWsDrCznBgC5SE88yiQubGqjUosVnHeHeC50J4mYpX75YikVDc6e6rE5FyYIbs2nOVJ4vts5NE3lEeDzA9y1+netSIhEKId8yO8ygIFYB/dsRDONrEwVU9ukHhQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b9a0c840b412fc09a282eca1ef1dbb56')

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
    message = TextSendMessage(text="你說的是不是:" + event.message.text)
    line_bot_api.reply_message(event.reply_token, message)    

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
