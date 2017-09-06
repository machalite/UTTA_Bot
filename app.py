from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from flask import Flask, request, abort
from linebot.models import *
from strings import *
from functions import *

app = Flask(__name__)
line_bot_api = LineBotApi('DUTE1UOjEqCQpJynGDa59KSV42WXmVjM8/Dw2qaFuyA9ePaA40Qy2lHRcfRaM0SzM3HpvNYySB2IrkJGiQ+1RktH1Ko6285vipalBZ8WtDy+6T1pRZDnS/NHDvUgadaxLCR0TbACjTKRyZkMpOjYUgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a62c4f246f3dfe799fa69c44d9d99a82')


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
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)
    if event.message.text == "coba":
        content = "Berhasil !!"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 'OK'
    if event.message.text == "!about":
        content = Strings().ABOUT
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 'OK'
    if event.message.text == "!user":
        content = selUser()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 'OK'
    if event.message.text == "!commands":
        buttons_template = TemplateSendMessage(
            alt_text=Strings().ERR_PC,
            template=ButtonsTemplate(
                title='List of Commands',
                text='Select a command',
                # thumbnail_image_url=Strings().IMGUR_UTTA,
                actions=[
                    MessageTemplateAction(
                        label=Strings().REGISTER,
                        text=Strings().INST_REGISTER
                    ),
                    MessageTemplateAction(
                        label=Strings().TODAY,
                        text=Strings().TODAY
                    ),
                    MessageTemplateAction(
                        label=Strings().ROOMCHECK,
                        text=Strings().ROOMCHECK
                    ),
                    MessageTemplateAction(
                        label=Strings().HELP,
                        text=Strings().HELP
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
    return 'OK'


if __name__ == '__main__':
    app.run()
