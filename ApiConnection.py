import requests
import os
import csv
from Globals import credentials_csv_path,access_data_csv_path,token_data_csv_path,select_version, state

class Connection:
    def __init__(self):
        self.client_id = None
        self.client_secret = None
        self.credentials_csv_file = credentials_csv_path

        if os.path.isfile(self.credentials_csv_file):
            self.load_credentials_from_csv(self.credentials_csv_file)
        else:
            self.client_secret = ""
            self.client_id = ""

        self.credentials_csv_path = credentials_csv_path
        self.access_data_csv_path = access_data_csv_path
        self.token_data_csv_path = token_data_csv_path

        urls = select_version(state)
        self.url_show_access_attempt_with_auth = urls['url_show_access_attempt_with_auth']
        self.url_access_attempt_with_auth = urls['url_access_attempt_with_auth']
        self.url_authenticate_with_credentials = urls['url_authenticate_with_credentials']

    def load_credentials_from_csv(self, csv_file):
        if os.path.isfile(csv_file):
            with open(csv_file, 'r', newline='', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.client_id = row['Client ID']
                    self.client_secret = row['Client Secret']
                    break

    def show_access_attempt_with_auth(self, index):
        self.load_credentials_from_csv(self.credentials_csv_path)
        try:
            endpoint = self.url_show_access_attempt_with_auth
            auth_data = {
                "ClientId": self.client_id,
                "ClientSecret": self.client_secret,
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

            self.response = requests.post(endpoint, json=auth_data)

            if self.response.status_code == 200:
                data = self.response.json()
                return data
            else:
                print("Połączenie z API nieudane: Status code " + str(self.response.status_code))

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")


    def access_attempt_with_auth(self, index):
        self.load_credentials_from_csv(self.credentials_csv_path)
        try:
            endpoint = self.url_access_attempt_with_auth
            auth_data = {
                "ClientId": self.client_id,
                "ClientSecret": self.client_secret,
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

            self.response = requests.post(endpoint, json=auth_data)

            if self.response.status_code == 200:
                data = self.response.json()
                self.save_data_to_csv(data, self.access_data_csv_path)
                self.save_credentials_to_csv(self.client_id, self.client_secret,data, self.credentials_csv_path)
                print("Połączenie z API udane, zalagowano jako: "+str(data['items'][0]['name']))
                self.authenticate_with_credentials(self.credentials_csv_path, self.token_data_csv_path)
                return True
            else:
                print("Połączenie z API nieudane: Status code " + str(self.response.status_code))
                return False


        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return False



    def authenticate_with_credentials(self, credentials_file, token_file):
        try:

            with open(credentials_file, 'r', newline='', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    client_id = row.get('Client ID', '')
                    client_secret = row.get('Client Secret', '')
                    eup_id = row.get('eupId', '')
                    break

            if client_id and client_secret and eup_id:

                auth_data = {
                    "ClientId": client_id,
                    "ClientSecret": client_secret,
                    "EupId": eup_id
                }

                url = self.url_authenticate_with_credentials

                response = requests.post(url, json=auth_data)

                if response.status_code == 200:
                    data = response.json()
                    AccessToken = data['AccessToken']
                    TokenType = data['TokenType']
                    ExpiresIn = data['ExpiresIn']

                    with open(token_file, 'w', newline='', encoding='utf-8-sig') as token_csv:
                        fieldnames = ['AccessToken', 'TokenType', 'ExpiresIn']
                        writer = csv.DictWriter(token_csv, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerow({'AccessToken': AccessToken, 'TokenType': TokenType, 'ExpiresIn': ExpiresIn})

                else:

                    print(f"Błąd {response.status_code}: {response.text}")
            else:
                print("Brak danych uwierzytelniających w pliku CSV.")

        except Exception as e:
            print(f"Wystąpił błąd podczas autoryzacji: {e}")

    @staticmethod
    def save_data_to_csv(data, csv_file):
        with open(csv_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['pageSize', 'pageNumber', 'totalPagesNumber', 'totalResultNumber', 'hasPreviousPage',
                          'hasNextPage', 'eupId', 'companyId', 'name', 'identificationNumber', 'province',
                          'district', 'commune', 'locality', 'street', 'buildingNumber', 'localNumber',
                          'addressHtml', 'isActive']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for item in data['items']:
                writer.writerow({
                    'pageSize': data['pageSize'],
                    'pageNumber': data['pageNumber'],
                    'totalPagesNumber': data['totalPagesNumber'],
                    'totalResultNumber': data['totalResultNumber'],
                    'hasPreviousPage': data['hasPreviousPage'],
                    'hasNextPage': data['hasNextPage'],
                    'eupId': item['eupId'],
                    'companyId': item['companyId'],
                    'name': item['name'],
                    'identificationNumber': item['identificationNumber'],
                    'province': item['province'],
                    'district': item['district'],
                    'commune': item['commune'],
                    'locality': item['locality'],
                    'street': item['street'],
                    'buildingNumber': item['buildingNumber'],
                    'localNumber': item['localNumber'],
                    'addressHtml': item['addressHtml'],
                    'isActive': item['isActive']
                })

    @staticmethod
    def save_credentials_to_csv(client_id, client_secret, data, csv_file):
        eup_id = data['items'][0]['eupId']
        with open(csv_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['Client ID', 'Client Secret', 'eupId']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'Client ID': client_id, 'Client Secret': client_secret, 'eupId': eup_id})


class GetToken:
    def __init__(self, number):
        pass




    @staticmethod
    def read_access_token_from_csv():
        dir_path = os.path.dirname(os.path.realpath(__file__))
        csv_file = os.path.join(dir_path, "temp/Token_data.csv")
        try:
            with open(csv_file, 'r', newline='', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    return {
                        'AccessToken': row['AccessToken'],
                        'TokenType': row['TokenType'],
                        'ExpiresIn': row['ExpiresIn'],
                    }

        except FileNotFoundError:
            print(f"Plik {csv_file} nie został znaleziony.")
        except KeyError:
            print(f"Błędny format danych w pliku {csv_file}.")
        except Exception as e:
            print(f"Wystąpił błąd podczas odczytu pliku {csv_file}: {e}")

        return {}


if __name__ == '__main__':
    conn = Connection()



    conn.access_attempt_with_auth(1)
