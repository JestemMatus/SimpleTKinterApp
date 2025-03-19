import requests

def access_attempt_with_auth(index):
    endpoint = "https://rejestr-bdo.mos.gov.pl/api/WasteRegister/v1/Auth/getEupList"
    auth_data = {
        "ClientId": "6c06693a-2054-49b8-93d2-f2b4f5ce36f5",
        "ClientSecret": "7e4582f5766a4654ab8a3d06a6a9a8e147ada0ab62bd45dcb9a7a4afcaad0666",
        "PaginationParameters": {
            "Order": {
                "IsAscending": True
            },
            "Page": {
                "Index": index,
                "Size": 0,
            }
        }
    }
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    response = requests.post(endpoint, json=auth_data, headers=headers)

    if response.status_code == 200:
        try:
            data = response.json()
            print("Połączenie z API udane, zalogowano jako:", data['items'][0]['name'])
        except requests.exceptions.JSONDecodeError as json_err:
            print(f"Połączenie z API nieudane: Błąd dekodowania JSON: {json_err}")
            print(f"Surowa odpowiedź z API: {response.text}")
    else:
        print(f"Połączenie z API nieudane: Kod statusu {response.status_code}")
        print(f"Odpowiedź z API: {response.text}")


def access_attempt_with_auth2(index):
    try:
        endpoint = "https://rejestr-bdo.mos.gov.pl/api/WasteRegister/v1/Auth/getEupList"
        auth_data = {
            "ClientId": "6c06693a-2054-49b8-93d2-f2b4f5ce36f5",
            "ClientSecret": "7e4582f5766a4654ab8a3d06a6a9a8e147ada0ab62bd45dcb9a7a4afcaad0666",
            "PaginationParameters": {
                "Order": {
                    "IsAscending": True
                },
                "Page": {
                    "Index": index,
                    "Size": 0,
                }
            }
        }

        response = requests.post(endpoint, json=auth_data)

        if response.status_code == 200:
            data = response.json()
            print("Połączenie z API udane, zalagowano jako: "+str(data['items'][0]['name']))
            return True
        else:
            print("Połączenie z API nieudane: Status code " + str(response.status_code))
            return False


    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return False

access_attempt_with_auth2(2)
