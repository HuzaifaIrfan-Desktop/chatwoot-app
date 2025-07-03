
from pydantic import EmailStr, ValidationError

from settings import Settings

settings = Settings()

print("Chatwoot URL:", settings.chatwoot_url)
print("Inbox Identifier:", settings.inbox_identifier)
print("Contact Identifier:", settings.contact_identifier)

import json
from pprint import pprint


import requests

# https://developers.chatwoot.com/api-reference/introduction
## Chatwoot Client APIs - Contacts API

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
    
    try:
        print(response.json())

        return response.json()
    except:
        print(response)

        return {"source_id":None, "pubsub_token": None}


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


## Chatwoot Client APIs - Conversations API

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

    pprint(response.json())

    try:
        if isinstance(response.json(), list):
            if len(response.json()) <= 0:
                return {"id":None}
            else:
                return response.json()[0]
    except:
        pass

    try:
        if response.json()["status"]==404:
            print("get_conversation status 404")
            return {"id":None}
    except:
        pass
 


    return response.json()



def resolve_conversation(contact_identifier: str, conversation_id: str):

    url = f"{settings.chatwoot_url}/public/api/v1/inboxes/{settings.inbox_identifier}/contacts/{contact_identifier}/conversations/{conversation_id}/toggle_status"

    response = requests.request("POST", url)

    print(response.json())

    return response.json()


def toggle_typing_status_on(contact_identifier: str, conversation_id: str):

    url = f"{settings.chatwoot_url}/public/api/v1/inboxes/{settings.inbox_identifier}/contacts/{contact_identifier}/conversations/{conversation_id}/toggle_typing"

    payload = {"typing_status": "on"}
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.json())

    return response.json()

def toggle_typing_status_off(contact_identifier: str, conversation_id: str):

    url = f"{settings.chatwoot_url}/public/api/v1/inboxes/{settings.inbox_identifier}/contacts/{contact_identifier}/conversations/{conversation_id}/toggle_typing"

    payload = {"typing_status": "off"}
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.json())

    return response.json()



def update_last_seen(contact_identifier: str, conversation_id: str):

    url = f"{settings.chatwoot_url}/public/api/v1/inboxes/{settings.inbox_identifier}/contacts/{contact_identifier}/conversations/{conversation_id}/update_last_seen"

    response = requests.request("POST", url)

    print(response.json())

    return response.json()


## Chatwoot Client APIs - Messages API

def list_messages(contact_identifier: str, conversation_id: str):

    url = f"{settings.chatwoot_url}/public/api/v1/inboxes/{settings.inbox_identifier}/contacts/{contact_identifier}/conversations/{conversation_id}/messages"

    response = requests.request("GET", url)

    print(response.json())

    return response.json()

def create_message(contact_identifier: str, conversation_id: str, message: str):

    url = f"{settings.chatwoot_url}/public/api/v1/inboxes/{settings.inbox_identifier}/contacts/{contact_identifier}/conversations/{conversation_id}/messages"

    payload = {
        "content": message,
        "echo_id": "1234567890"
    }
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.json())

    return response.json()

def update_message(contact_identifier: str, conversation_id: str, message_id: str):

    url = f"{settings.chatwoot_url}/public/api/v1/inboxes/{settings.inbox_identifier}/contacts/{contact_identifier}/conversations/{conversation_id}/messages/{message_id}"

    payload = {"submitted_values": {
            "name": "My Name",
            "title": "My Title",
            "value": "value",
            "csat_survey_response": {
                "feedback_message": "Great service!",
                "rating": 5
            }
        }}
    headers = {"Content-Type": "application/json"}

    response = requests.request("PATCH", url, json=payload, headers=headers)

    print(response.json())

    return response.json()
