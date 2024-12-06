import json

def process_notification(body):
    try:
        message = json.loads(body)
        notification_type = message.get("type")
        user_id = message.get("user_id")
        content = message.get("content")

        print(f"[Notification] Type: {notification_type}, User ID: {user_id}, Content: {content}")
    except Exception as e:
        print(f"Failed to process notification: {e}")
