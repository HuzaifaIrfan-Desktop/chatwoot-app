

from chatwoot import Chatwoot

from chatwoot.client_apis import create_contact, get_contact, update_contact
from chatwoot.client_apis import list_conversations, create_conversation, get_conversation, resolve_conversation, toggle_typing_status_on, toggle_typing_status_off, update_last_seen
from chatwoot.client_apis import  list_messages, create_message, update_message



def test_client_apis():
    email="pytest@chatwoot.home"
    name="pytest"
    contact = create_contact(email, name)
    contact_identifier:str = contact["source_id"]
    pubsub_token:str = contact["pubsub_token"]

    # update_contact(contact_identifier, "update@chatwoot.home", "update")
    get_contact(contact_identifier)

    conversation=create_conversation(contact_identifier)
    conversation_id=str(conversation["id"])

    list_conversations(contact_identifier)
    get_conversation(contact_identifier, conversation_id)

    message=create_message(contact_identifier, conversation_id, "Chatwoot Client APIs Test")
    message_id=str(message["id"])

    update_message(contact_identifier, conversation_id, message_id)
    list_messages(contact_identifier, conversation_id)


def test_chatwoot_integration():
    email="pytest@chatwoot.home"
    name="pytest"
        
    chatwoot = Chatwoot(lambda sender_name, agent_content : print(f"{sender_name} : {agent_content}"), email, name)

    chatwoot.send_message("pytest")

    # chatwoot.run_websocket()
