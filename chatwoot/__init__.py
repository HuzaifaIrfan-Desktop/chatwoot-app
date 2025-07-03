
from pydantic import EmailStr, ValidationError

from settings import Settings

settings = Settings()

print("Chatwoot URL:", settings.chatwoot_url)
print("Inbox Identifier:", settings.inbox_identifier)
print("Contact Identifier:", settings.contact_identifier)


import requests

def create_contact(email: EmailStr, name:str, phone_number:str= ""):

    url = f"{settings.chatwoot_url}/public/api/v1/inboxes/{settings.inbox_identifier}/contacts"

    payload = {
        # "identifier": "1234567890",
        # "identifier_hash": ,
        "email": email,
        "name": name,
        "phone_number": phone_number,
        "custom_attributes": {}
    }
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.json())

    return response.json()



def get_contact(contact_identifier: str):
    url = f"{settings.chatwoot_url}/public/api/v1/inboxes/{settings.inbox_identifier}/contacts/{contact_identifier}"

    response = requests.request("GET", url)

    print(response.json())

    return response.json()


def update_contact(contact_identifier: str, email: EmailStr, name:str, phone_number:str= ""):

    url = f"{settings.chatwoot_url}/public/api/v1/inboxes/{settings.inbox_identifier}/contacts/{contact_identifier}"

    payload = {
        # "identifier": "1234567890",
        # "identifier_hash": ,
        "email": email,
        "name": name,
        "phone_number": phone_number,
        "custom_attributes": {}
    }
    headers = {"Content-Type": "application/json"}

    response = requests.request("PATCH", url, json=payload, headers=headers)

    print(response.json())

    return response.json()



def list_conversations(contact_identifier: str):
    url = f"{settings.chatwoot_url}/public/api/v1/inboxes/{settings.inbox_identifier}/contacts/{contact_identifier}/conversations"

    response = requests.request("GET", url)

    print(response.json())

    return response.json()

def create_conversation(contact_identifier: str):
    url = f"{settings.chatwoot_url}/public/api/v1/inboxes/{settings.inbox_identifier}/contacts/{contact_identifier}/conversations"

    payload = {"custom_attributes": {}}
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.json())

    return response.json()

def get_conversation(contact_identifier: str, conversation_id: str):
    url = f"{settings.chatwoot_url}/public/api/v1/inboxes/{settings.inbox_identifier}/contacts/{contact_identifier}/conversations/{conversation_id}"

    response = requests.request("GET", url)

    print(response.json())

    return response.json()