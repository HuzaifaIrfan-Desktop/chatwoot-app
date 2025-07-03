

from chatwoot import create_contact, get_contact, update_contact
from chatwoot import list_conversations, create_conversation, get_conversation
from chatwoot import  list_messages, create_message, update_message


contact = create_contact("test@chatwoot.home", "test")
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

def main():
    pass


if __name__ == "__main__":
    main()