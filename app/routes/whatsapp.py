import os, requests, json, logging
from flask import Blueprint, request, jsonify

# Blueprint setup
whatsapp_bp = Blueprint("whatsapp", __name__, url_prefix="/whatsapp")

# Environment variables
VERIFY_TOKEN = os.getenv("WA_VERIFY_TOKEN", "acms_verify_token")
ACCESS_TOKEN = os.getenv("WA_ACCESS_TOKEN")
PHONE_ID = os.getenv("WA_PHONE_ID")

# WhatsApp message sender
def send_whatsapp(to: str, text: str):
    if not ACCESS_TOKEN:
        logging.warning("WhatsApp disabled – no ACCESS_TOKEN set")
        return
    url = f"https://graph.facebook.com/v19.0/{PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        logging.info(f"WA send response: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        logging.exception("Failed to send WhatsApp message")

# Webhook handler
@whatsapp_bp.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Webhook verification
        verify_token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if verify_token == VERIFY_TOKEN:
            return challenge, 200
        return "Invalid verify token", 403

    # POST request: Handle incoming messages
    try:
        data = request.get_json()
        logging.debug(f"Incoming WhatsApp data: {json.dumps(data, indent=2)}")

        entry = data["entry"][0]["changes"][0]["value"]
        messages = entry.get("messages")
        if messages:
            message = messages[0]
            sender = message["from"]
            text = message["text"]["body"]

            # Call your chatbot logic
            try:
                from app.utils.chatbot import get_response
                reply = get_response(text)
            except ImportError:
                reply = f"You said: {text}"

            send_whatsapp(sender, reply)
        else:
            logging.info("No message found in incoming payload")

    except Exception as e:
        logging.exception("Error handling WhatsApp webhook")

    return "OK", 200
