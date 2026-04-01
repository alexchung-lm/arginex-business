"""ArgiNex S1 — LINE Bot 客製化酒標服務"""

import os
from flask import Flask, request, abort, send_from_directory
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    MessagingApiBlob,
    ReplyMessageRequest,
    TextMessage,
    ImageMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent, ImageMessageContent
from linebot.v3.webhook import WebhookParser
from label_engine import generate_custom_label

# ---------- Config ----------
CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
BASE_URL = os.environ.get("BASE_URL", "http://localhost:10000")
PORT = int(os.environ.get("PORT", 10000))

app = Flask(__name__)
parser = WebhookParser(CHANNEL_SECRET)
config = Configuration(access_token=CHANNEL_ACCESS_TOKEN)

# ---------- 對話狀態 ----------
IDLE = "IDLE"
WAITING_NAME = "WAITING_NAME"
WAITING_LOGO = "WAITING_LOGO"
WAITING_CONFIRM = "WAITING_CONFIRM"

user_states: dict[str, dict] = {}


def get_state(user_id: str) -> dict:
    if user_id not in user_states:
        user_states[user_id] = {"step": IDLE, "company_name": ""}
    return user_states[user_id]


def reset_state(user_id: str):
    user_states.pop(user_id, None)


# ---------- Routes ----------
@app.route("/ping")
def ping():
    return "pong"


@app.route("/images/<path:filename>")
def serve_image(filename):
    return send_from_directory("output", filename)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        events = parser.parse(body, signature)
    except Exception:
        abort(400)

    with ApiClient(config) as api_client:
        messaging_api = MessagingApi(api_client)
        blob_api = MessagingApiBlob(api_client)

        for event in events:
            if not isinstance(event, MessageEvent):
                continue
            handle_message(event, messaging_api, blob_api)

    return "OK"


def reply(messaging_api: MessagingApi, token: str, messages: list):
    messaging_api.reply_message(
        ReplyMessageRequest(reply_token=token, messages=messages)
    )


def handle_message(
    event: MessageEvent,
    messaging_api: MessagingApi,
    blob_api: MessagingApiBlob,
):
    user_id = event.source.user_id
    state = get_state(user_id)

    # 「重新開始」→ 任何狀態都回 IDLE
    if isinstance(event.message, TextMessageContent) and event.message.text.strip() == "重新開始":
        reset_state(user_id)
        reply(messaging_api, event.reply_token, [
            TextMessage(text="已重新開始。請問您的公司名稱是？"),
        ])
        get_state(user_id)["step"] = WAITING_NAME
        return

    step = state["step"]

    # --- IDLE ---
    if step == IDLE:
        state["step"] = WAITING_NAME
        reply(messaging_api, event.reply_token, [
            TextMessage(text="歡迎！我是 ArgiNex 客製化果酒助理。請問您的公司名稱是？"),
        ])

    # --- WAITING_NAME ---
    elif step == WAITING_NAME:
        if not isinstance(event.message, TextMessageContent):
            reply(messaging_api, event.reply_token, [
                TextMessage(text="請輸入您的公司名稱（文字）"),
            ])
            return
        company_name = event.message.text.strip()
        state["company_name"] = company_name
        state["step"] = WAITING_LOGO
        reply(messaging_api, event.reply_token, [
            TextMessage(text=f"{company_name} 您好！請傳送您的公司 Logo 圖片"),
        ])

    # --- WAITING_LOGO ---
    elif step == WAITING_LOGO:
        if not isinstance(event.message, ImageMessageContent):
            reply(messaging_api, event.reply_token, [
                TextMessage(text="請傳送一張圖片作為 Logo"),
            ])
            return

        try:
            # 下載圖片
            message_id = event.message.id
            print(f"[LOGO] 下載圖片 message_id={message_id}")
            content = blob_api.get_message_content(message_id)
            # SDK v3 可能回傳 bytes 或 response object
            if hasattr(content, 'read'):
                content = content.read()
            elif hasattr(content, 'content'):
                content = content.content
            logo_path = os.path.join("uploads", f"{user_id}_logo.png")
            with open(logo_path, "wb") as f:
                f.write(content)
            print(f"[LOGO] 圖片已存到 {logo_path}, 大小={os.path.getsize(logo_path)}")

            # 生成酒標
            company_name = state["company_name"]
            print(f"[LOGO] 開始生成酒標: {company_name}")
            output_path = generate_custom_label(company_name, logo_path)
            print(f"[LOGO] 酒標生成完成: {output_path}")
            filename = os.path.basename(output_path)
            image_url = f"{BASE_URL}/images/{filename}"
            print(f"[LOGO] 圖片 URL: {image_url}")

            state["step"] = WAITING_CONFIRM
            reply(messaging_api, event.reply_token, [
                ImageMessage(original_content_url=image_url, preview_image_url=image_url),
                TextMessage(
                    text=f"這是為 {company_name} 製作的專屬酒標，請確認是否滿意？\n回覆「確認」下單，「重做」重新設計"
                ),
            ])
        except Exception as e:
            print(f"[ERROR] 酒標生成失敗: {e}")
            import traceback; traceback.print_exc()
            reply(messaging_api, event.reply_token, [
                TextMessage(text=f"抱歉，酒標生成時發生錯誤：{str(e)[:100]}\n請重新傳送 Logo 圖片試試"),
            ])

    # --- WAITING_CONFIRM ---
    elif step == WAITING_CONFIRM:
        if not isinstance(event.message, TextMessageContent):
            reply(messaging_api, event.reply_token, [
                TextMessage(text="請回覆「確認」下單，或「重做」重新設計"),
            ])
            return

        text = event.message.text.strip()
        if text == "確認":
            reply(messaging_api, event.reply_token, [
                TextMessage(text="已確認！我們會盡快安排印刷。"),
            ])
            reset_state(user_id)
        elif text == "重做":
            state["step"] = WAITING_LOGO
            reply(messaging_api, event.reply_token, [
                TextMessage(text="沒問題！請重新傳送 Logo 圖片"),
            ])
        else:
            reply(messaging_api, event.reply_token, [
                TextMessage(text="請回覆「確認」下單，或「重做」重新設計"),
            ])


# ---------- Startup ----------
if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    app.run(host="0.0.0.0", port=PORT)
