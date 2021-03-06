from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from flask import Flask, request, abort
from linebot.models import *
from settings import *
from strings import *
from functions import *

app = Flask(__name__)
line_bot_api = LineBotApi(Settings().CHANNEL_TOKEN)
handler = WebhookHandler(Settings().CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # print("body:",body)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 200


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # get user profile
    profile = line_bot_api.get_profile(event.source.user_id)
    # Contains user input message
    inputMsg = str(event.message.text)
    # Print user input on console
    print(Strings().CONS_INPUT, event.message.text)

    if inputMsg.startswith(Strings().REGISTER):
        index = len(Strings().REGISTER) + 1
        authCode = inputMsg[index:]
        content = register(authCode, profile.user_id)

    elif inputMsg == Strings().TODAY:
        content = today(profile.user_id)

    elif inputMsg.startswith(Strings().CHECKROOM):
        index = len(Strings().CHECKROOM) + 1
        roomInput = inputMsg[index:]
        content = checkroom(roomInput, profile.user_id)

    elif inputMsg == Strings().SCHEDULE:
        content = schedule(profile.user_id)

    elif inputMsg == Strings().NEXT:
        content = next(profile.user_id)

    elif inputMsg.startswith(Strings().WHERE):
        index = len(Strings().WHERE) + 1
        roomInput = inputMsg[index:]
        content = where(roomInput, profile.user_id)

    elif inputMsg.startswith(Strings().CHECKCOURSE):
        index = len(Strings().CHECKCOURSE) + 1
        courseInput = inputMsg[index:]
        content = checkcourse(courseInput, profile.user_id)

    elif inputMsg == Strings().CHANGES:
        content = changes(profile.user_id)

    elif inputMsg == Strings().ABOUT:
        content = Strings().ABOUT_CONTENT

    elif inputMsg == Strings().HELP:
        content = Strings().HELP_CONTENT

    else:
        content = Strings().HELP_CONTENT

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))

    return 'OK'


if __name__ == '__main__':
    app.run()
