"""Examples for webhook management and handling."""

from asaas import Asaas

client = Asaas(api_key="your_api_key_here", sandbox=True)

# -- Register a webhook --
webhook = client.webhooks.create(
    url="https://yoursite.com/api/asaas/webhook",
    email="admin@yoursite.com",
    enabled=True,
    api_version=3,
    auth_token="your_webhook_secret_token",
    events=[
        "PAYMENT_CREATED",
        "PAYMENT_UPDATED",
        "PAYMENT_CONFIRMED",
        "PAYMENT_RECEIVED",
        "PAYMENT_OVERDUE",
        "PAYMENT_REFUNDED",
        "PAYMENT_DELETED",
        "PAYMENT_CHARGEBACK_REQUESTED",
    ],
)
print(f"Webhook created: {webhook['id']}")

# -- List webhooks --
page = client.webhooks.list()
for wh in page.data:
    print(f"  {wh['id']} - {wh['url']} - enabled={wh.get('enabled')}")

# -- Update a webhook --
client.webhooks.update(webhook["id"], enabled=False)
print("Webhook disabled")

# -- Remove backoff penalty --
# If your webhook endpoint had errors and got penalized:
# client.webhooks.remove_backoff(webhook["id"])


# ==============================================================
# Example: Flask webhook handler
# ==============================================================
#
# from flask import Flask, request, jsonify
#
# app = Flask(__name__)
# WEBHOOK_TOKEN = "your_webhook_secret_token"
#
# @app.route("/api/asaas/webhook", methods=["POST"])
# def handle_webhook():
#     token = request.headers.get("asaas-access-token")
#     if token != WEBHOOK_TOKEN:
#         return jsonify({"error": "unauthorized"}), 401
#
#     event = request.json
#     event_type = event.get("event")
#     payment = event.get("payment", {})
#
#     if event_type == "PAYMENT_CONFIRMED":
#         print(f"Payment confirmed: {payment['id']} - R${payment['value']}")
#         # Update your order status, grant access, etc.
#
#     elif event_type == "PAYMENT_OVERDUE":
#         print(f"Payment overdue: {payment['id']}")
#         # Send reminder, suspend access, etc.
#
#     elif event_type == "PAYMENT_REFUNDED":
#         print(f"Payment refunded: {payment['id']}")
#         # Process refund in your system
#
#     return jsonify({"received": True}), 200


client.close()
