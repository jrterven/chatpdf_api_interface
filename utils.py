import os
import sys
import requests


def get_api_key(var_name):
    """
    Retrieve the API key from environment variables and exit the program if not found.

    :return: str, API key if found
    """
    api_key = os.environ.get(var_name)

    if not api_key:
        print(f"{var_name} key not found.")
        sys.exit()

    return api_key


def upload_chatpdf_file(file_path, chatpdf_api_key):
    files = [
        ('file', ('file', open(file_path, 'rb'), 'application/octet-stream'))
    ]
    headers = {
        'x-api-key': chatpdf_api_key
    }

    response = requests.post(
        'https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files)

    print(f"Status code={response.status_code}")
    
    if response.status_code == 200:
        print("File uploaded successfully")
        source_id = response.json()['sourceId']
        print(f'Source ID: {source_id}')
        return source_id
    else:
        print('Status:', response.status_code)
        print('Error:', response.text)
        return None
    

def query_chatpdf(chatpdf_api_key, source_id, prompt):
    data = {
      "sourceId": source_id,
      "messages": [
        {
          "role": "user",
          "content": prompt
        }
      ]
    }

    headers = {
      'x-api-key': chatpdf_api_key,
      'Content-Type': 'application/json',
    }

    response = requests.post(
      'https://api.chatpdf.com/v1/chats/message', json=data, headers=headers)

    if response.status_code == 200:
        result = response.json()['content']
        return result
    else:
        print('Status:', response.status_code)
        print('Error:', response.text)
        return None