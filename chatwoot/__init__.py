

from chatwoot.client_apis import create_contact, get_contact, update_contact
from chatwoot.client_apis import list_conversations, create_conversation, get_conversation, resolve_conversation, toggle_typing_status_on, toggle_typing_status_off, update_last_seen
from chatwoot.client_apis import  list_messages, create_message, update_message

import websocket
import json
from pprint import pprint


from settings import Settings

settings = Settings()

print("Chatwoot WS URL:", settings.chatwoot_ws_url)

class Chatwoot:
    def __init__(self, agent_reply):
        self.agent_reply=agent_reply
        
        self.ws_url = f"{settings.chatwoot_ws_url}cable"

        self.contact={}
        self.contact_identifier:str = ""
        self.pubsub_token:str = ""
        self.conversation={}
        self.conversation_id:str = ""

        self.setup_contact()
        self.setup_conversation()

        self.setup_websocket()

    def setup_contact(self):
        self.contact = create_contact("test@chatwoot.home", "test")
        self.contact_identifier:str = self.contact["source_id"]
        self.pubsub_token:str = self.contact["pubsub_token"]
        
    def setup_conversation(self):
        self.conversation=create_conversation(self.contact_identifier)
        self.conversation_id=str(self.conversation["id"])

    def send_message(self, message:str):
        message=create_message(self.contact_identifier, self.conversation_id, message)
        message_id=str(message["id"])


    def setup_websocket(self):

        websocket.enableTrace(False)  # Set to True for verbose logging

        self.ws = websocket.WebSocketApp(
            self.ws_url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )

    def run_websocket(self):
        self.ws.run_forever()
                


    def on_open(self, ws):
        print("🔗 Connection opened.") 

        identifier = {
            "channel": "RoomChannel",
            "pubsub_token": self.pubsub_token
        }

        message = {
            "command": "subscribe",
            "identifier": json.dumps(identifier)
        }

        self.ws.send(json.dumps(message))
        print("📨 Subscription sent.")

    def on_message(self, ws, message):
        # print("📥 Message received:")
        # try:
        #     parsed = json.loads(message)
        #     pprint(parsed)
        # except Exception:
        #     print(message)
        try:
            data = json.loads(message)

            msg_type = data.get("type")
            if msg_type == "welcome":
                pprint(data)
            elif msg_type == "ping":
                pprint(data)
            elif msg_type == "confirm_subscription":
                pprint(data)
            elif isinstance(data.get("message"), dict):
                event = data["message"].get("event")
                if event == "message.created":
                    msg_data = data["message"].get("data", {})
                    if msg_data.get("message_type") == 1:
                        sender_name = msg_data.get("sender", {}).get("name", "Unknown")
                        content = msg_data.get("content", "")
                        pprint(f"{sender_name} : {content}")
                        self.agent_reply(sender_name, content)
            else:
                print("🤔 Unknown message format:")
                pprint(data)

        except json.JSONDecodeError:
            print("❌ Failed to parse message as JSON:", message)

    def on_error(self, ws, error):
        print("❌ Error:")
        pprint(error)

    def on_close(self, ws, code, reason):
        print(f"🔌 Connection closed: code={code}, reason={reason}")
