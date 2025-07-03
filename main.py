

from chatwoot import create_contact, get_contact, update_contact, list_conversations, create_conversation, get_conversation

contact = create_contact("test@chatwoot.home", "test")
contact_identifier:str = contact["source_id"]

get_contact(contact_identifier)
# update_contact(contact_identifier, "update@chatwoot.home", "update")

list_conversations(contact_identifier)
conversation=create_conversation(contact_identifier)
conversation_id=str(conversation["id"])

def main():

    get_conversation(contact_identifier, conversation_id)




if __name__ == "__main__":
    main()