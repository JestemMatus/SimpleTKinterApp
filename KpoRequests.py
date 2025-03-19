import requests
import ApiConnection
import tkinter as tk
from tkinter import messagebox
import base64
from Globals import select_version, state

class KPO:
    def __init__(self):
        self.jwt_token_tuple = ApiConnection.GetToken.read_access_token_from_csv()
        self.jwt_token = self.jwt_token_tuple['AccessToken']

        urls = select_version(state)

        self.url_lista_kart_ze_statusem_zrealizowane_przejecie = urls['url_lista_kart_ze_statusem_zrealizowane_przejecie']
        self.url_szczegoly_karty_planowana = urls['url_szczegoly_karty_planowana']
        self.url_szczegoly_karty_wycofana = urls['url_szczegoly_karty_wycofana']
        self.url_szczegoly_karty_zatwierdzona = urls['url_szczegoly_karty_zatwierdzona']
        self.url_szczegoly_karty_wygenerowane_potwierdzenie = urls['url_szczegoly_karty_wygenerowane_potwierdzenie']
        self.url_szczegoly_karty_wygenerowane_potwierdzone_przyjecie = urls['url_szczegoly_karty_wygenerowane_potwierdzone_przyjecie']
        self.url_szczegoly_karty_odrzucona = urls['url_szczegoly_karty_odrzucona']
        self.url_szczegoly_karty_potwierdzony_transport = urls['url_szczegoly_karty_potwierdzony_transport']
        self.url_tworzenie_karty_ze_statusem_planowana = urls['url_tworzenie_karty_ze_statusem_planowana']
        self.url_wyszukiwarka_kart = urls['url_wyszukiwarka_kart']
        self.url_wyszukiwarka_kart_transportujacy = urls['url_wyszukiwarka_kart_transportujacy']
        self.url_wyszukiwarka_kart_przejmujacy = urls['url_wyszukiwarka_kart_przejmujacy']
        self.url_edycja_karty_ze_statusem_planowana = urls['url_edycja_karty_ze_statusem_planowana']
        self.url_edycja_karty_ze_statusem_zatwierdzona = urls['url_edycja_karty_ze_statusem_zatwierdzona']
        self.url_korekta_karty_odrzuconej = urls['url_korekta_karty_odrzuconej']
        self.url_zmiana_statusu_karty_z_planowanej_na_zatwierdzona = urls['url_zmiana_statusu_karty_z_planowanej_na_zatwierdzona']
        self.url_usuwanie_karty_ze_statusem_planowana = urls['url_usuwanie_karty_ze_statusem_planowana']
        self.url_zmiana_statusu_na_wycofana = urls['url_zmiana_statusu_na_wycofana']
        self.url_zmiana_statusu_na_odrzucona = urls['url_zmiana_statusu_na_odrzucona']
        self.url_zmiana_statusu_karty_z_wygenerowane_potwierdzenie_na_potwierdzenie_przyjecia = urls['url_zmiana_statusu_karty_z_wygenerowane_potwierdzenie_na_potwierdzenie_przyjecia']
        self.url_wygenerowanie_potwierdzenia_gdzie_podmiot_jest_transportujacy = urls['url_wygenerowanie_potwierdzenia_gdzie_podmiot_jest_transportujacy']
        self.url_wygenerowanie_potwierdzenia_gdzie_podmiot_jest_przekazujacy = urls['url_wygenerowanie_potwierdzenia_gdzie_podmiot_jest_przekazujacy']
        self.url_lista_kart_ze_statusem_zrealizowane_przejecie_lub_potwierdzony_transport_dla_przekazujacego = urls['url_lista_kart_ze_statusem_zrealizowane_przejecie_lub_potwierdzony_transport_dla_przekazujacego']
        self.url_zmiana_statusu_karty_na_potwierdzenie_wygenerowane = urls['url_zmiana_statusu_karty_na_potwierdzenie_wygenerowane']
        self.url_pobieranie_danych_do_wydruku = urls['url_pobieranie_danych_do_wydruku']
        self.url_wydruk = urls['url_wydruk']
        self.url_wydruk_karty = urls['url_wydruk_karty']
        self.url_zmiana_statusus_na_potwierdzenie_transportu = urls['url_zmiana_statusus_na_potwierdzenie_transportu']
        self.url_zwraca_liste_rekordow_zgodnie_z_wartoscia_zapytania = urls['url_zwraca_liste_rekordow_zgodnie_z_wartoscia_zapytania']
        self.url_wyszukiwarka_po_copmany_id = urls['url_wyszukiwarka_po_copmany_id']
        self.url_wyszukiwarka_dane_miejsca_po_eup_id = urls['url_wyszukiwarka_dane_miejsca_po_eup_id']
        self.url_zwroc_10_rekorwow_z_danymi_miejsc_prowadzenia_dzialanosci = urls['url_zwroc_10_rekorwow_z_danymi_miejsc_prowadzenia_dzialanosci']
        self.url_zwraca_liste_gmin = urls['url_zwraca_liste_gmin']
        self.url_zwraca_liste_gmin_po_id = urls['url_zwraca_liste_gmin_po_id']

    def lista_kart_ze_statusem_zrealizowane_przejecie(self):
        url = self.url_lista_kart_ze_statusem_zrealizowane_przejecie
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }

        params = {
            "PageSize": 10,
            "PaginationParameters.Order.IsAscending": True,
            "PaginationParameters.Order.OrderColumn": 1,
            "PaginationParameters.Page.Index": 1,
            "PaginationParameters.Page.Size": 5,
            "PaginationParameters.GetOrderColumn": None,
            "PaginationParameters.GetOrderDirection": "desc",
            "PaginationParameters.GetOrdering": None,
            "CardNumber": None,
            "SenderNip": None,
            "SenderIdentificationNumber": None,
            "SenderName": None,
            "ReceiveConfirmationTime": "2024-01-04T11:51:33.267Z",
            "CardStatusCodeNames": None,
            "WasteCodeName": None,
            "IsUsed": True,
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:

            data = response.json()
            print(data)
            return data
        else:

            data = (f"Błąd {response.status_code}: {response.text}")
            print(data)
            return data

    def szczegoly_karty_planowana(self,kpoId,rola):
        url = self.url_szczegoly_karty_planowana
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }

        params = {
            "kpoId": kpoId,
            "CompanyType": rola
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            print(data)
            return data
        else:

            data = (f"Błąd {response.status_code}: {response.text}")
            print(data)
            return data

    def szczegoly_karty_wycofana(self,kpoId,rola):
        url = self.url_szczegoly_karty_wycofana
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }

        params = {
            "kpoId": kpoId,
            "CompanyType": rola
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:

            data = response.json()
            print(data)
            return data
        else:

            data = (f"Błąd {response.status_code}: {response.text}")
            print(data)
            return data

    def szczegoly_karty_zatwierdzona(self,kpoId,rola):
        url = self.url_szczegoly_karty_zatwierdzona
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }

        params = {
            "kpoId": kpoId,
            "CompanyType": rola
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:

            data = response.json()
            print(data)
            return data
        else:

            data = (f"Błąd {response.status_code}: {response.text}")
            print(data)
            return data

    def szczegoly_karty_wygenerowane_potwierdzenie(self,kpoId,rola):
        url = self.url_szczegoly_karty_wygenerowane_potwierdzenie
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }

        params = {
            "kpoId": kpoId,
            "CompanyType": rola
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:

            data = response.json()
            print(data)
            return data
        else:

            data = (f"Błąd {response.status_code}: {response.text}")
            print(data)
            return data

    def szczegoly_karty_wygenerowane_potwierdzone_przyjecie(self,kpoId,rola):
        url = self.url_szczegoly_karty_wygenerowane_potwierdzone_przyjecie
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }

        params = {
            "kpoId": kpoId,
            "CompanyType": rola
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:

            data = response.json()
            print(data)
            return data
        else:

            data = (f"Błąd {response.status_code}: {response.text}")
            print(data)
            return data

    def szczegoly_karty_odrzucona(self,kpoId,rola):
        url = self.url_szczegoly_karty_odrzucona
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }

        params = {
            "kpoId": kpoId,
            "CompanyType": rola
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:

            data = response.json()
            print(data)
            return data
        else:

            data = (f"Błąd {response.status_code}: {response.text}")
            print(data)
            return data

    def szczegoly_karty_potwierdzony_transport(self,kpoId,rola):
        url = self.url_szczegoly_karty_potwierdzony_transport
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }

        params = {
            "kpoId": kpoId,
            "CompanyType": rola
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:

            data = response.json()
            print(data)
            return data
        else:

            data = (f"Błąd {response.status_code}: {response.text}")
            print(data)
            return data

    def tworzenie_karty_ze_statusem_planowana(self, data, parent):
        url = self.url_tworzenie_karty_ze_statusem_planowana
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            data = response.json()
            tk.messagebox.showinfo("Sukces", "Utworzono kartę planowaną", parent=parent)
            return data
        elif response.status_code == 201:
            data = response.json()
            tk.messagebox.showinfo("Sukces", "Utworzono kartę planowaną", parent=parent)
            return data
        else:
            tk.messagebox.showerror("Błąd",f"Odpowiedź serwera: Błąd {response.status_code}: {response.text}", parent=parent)
            return None

    def wyszukiwarka_kart(self, index, size, isAscending):
        url = self.url_wyszukiwarka_kart
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }


        data = {
          "PaginationParameters": {
            "Order": {
              "IsAscending": isAscending,
              "OrderColumn": "string"
            },
            "Page": {
              "Index": index,
              "Size": size
            }
          },
          "Year": None,
          "SearchInCarriers": False,
          "SearchInReceivers": False,
          "Name": None,
          "Locality": None,
          "Street": None,
          "Nip": None,
          "IdentificationNumber": None,
          "WasteCodeAndDescription": None,
          "CardNumber": None,
          "CardStatusCodeNames": None,
          "TransportTime": None,
          "ReceiveConfirmationTime": None,
          "SenderFirstNameAndLastName": None,
          "ReceiverFirstNameAndLastName": None,
          "VehicleRegNumber": None,
          "TransportDateRange": False,
          "TransportDateFrom": None,
          "TransportDateTo": None,
          "ReceiveConfirmationDateRange": False,
          "ReceiveConfirmationDateFrom": None,
          "ReceiveConfirmationDateTo": None,
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:

            data = response.json()
            return data
        elif response.status_code == 201:

            data = response.json()
            return data
        else:

            return None

    def wyszukiwarka_kart_transportujacy(self, index, size, isAscending):
        url = self.url_wyszukiwarka_kart_transportujacy
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }


        data = {
          "PaginationParameters": {
            "Order": {
              "IsAscending": isAscending,
              "OrderColumn": "string"
            },
            "Page": {
              "Index": index,
              "Size": size
            }
          },
          "Year": None,
          "SearchInSenders": False,
          "SearchInReceivers": False,
          "Name": None,
          "Locality": None,
          "Street": None,
          "Nip": None,
          "IdentificationNumber": None,
          "WasteCodeAndDescription": None,
          "CardNumber": None,
          "CardStatusCodeNames": None,
          "TransportTime": None,
          "ReceiveConfirmationTime": None,
          "SenderFirstNameAndLastName": None,
          "ReceiverFirstNameAndLastName": None,
          "VehicleRegNumber": None,
          "TransportDateRange": False,
          "TransportDateFrom": None,
          "TransportDateTo": None,
          "ReceiveConfirmationDateRange": False,
          "ReceiveConfirmationDateFrom": None,
          "ReceiveConfirmationDateTo": None,
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:

            data = response.json()
            print(data)
            return data
        elif response.status_code == 201:

            data = response.json()
            print(data)
            return data
        else:
            return None

    def wyszukiwarka_kart_przejmujacy(self, index, size, isAscending):
        url = self.url_wyszukiwarka_kart_przejmujacy
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }


        data = {
            "PaginationParameters": {
                "Order": {
                    "IsAscending": isAscending,
                    "OrderColumn": "string"
                },
                "Page": {
                    "Index": index,
                    "Size": size
                }
            },
            "Year": None,
            "SearchInSenders": False,
            "SearchInCarriers": False,
            "Name": None,
            "Locality": None,
            "Street": None,
            "Nip": None,
            "IdentificationNumber": None,
            "WasteCodeAndDescription": None,
            "CardNumber": None,
            "CardStatusCodeNames": None,
            "TransportTime": None,
            "ReceiveConfirmationTime": None,
            "SenderFirstNameAndLastName": None,
            "ReceiverFirstNameAndLastName": None,
            "VehicleRegNumber": None,
            "TransportDateRange": False,
            "TransportDateFrom": None,
            "TransportDateTo": None,
            "ReceiveConfirmationDateRange": False,
            "ReceiveConfirmationDateFrom": None,
            "ReceiveConfirmationDateTo": None,
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:

            data = response.json()
            return data
        elif response.status_code == 201:

            data = response.json()
            return data
        else:
            return None

    def edycja_karty_ze_statusem_planowana(self, data, parent):
        url = self.url_edycja_karty_ze_statusem_planowana
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }

        response = requests.put(url, headers=headers, json=data)

        if response.status_code == 200:

            data = response.json()
            tk.messagebox.showinfo("Sukces", "Edytowano kartę planowaną", parent=parent)
            return data
        elif response.status_code == 201:

            data = response.json()
            tk.messagebox.showinfo("Sukces", "Edytowano kartę planowaną", parent=parent)
            return data
        else:

            tk.messagebox.showerror("Błąd",f"Odpowiedź serwera: Błąd {response.status_code}: {response.text}", parent=parent)
            return None

    def edycja_karty_ze_statusem_zatwierdzona(self, data, parent):
        url = self.url_edycja_karty_ze_statusem_zatwierdzona
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }

        response = requests.put(url, headers=headers, json=data)

        if response.status_code == 200:

            data = response.json()
            tk.messagebox.showinfo("Sukces", "Edytowano kartę zatwierdzoną", parent=parent)
            return data
        elif response.status_code == 201:

            data = response.json()
            tk.messagebox.showinfo("Sukces", "Edytowano kartę zatwierdzoną", parent=parent)
            return data
        elif response.status_code == 204:


            tk.messagebox.showinfo("Sukces", "Edytowano kartę zatwierdzoną", parent=parent)

        else:

            tk.messagebox.showerror("Błąd",f"Odpowiedź serwera: Błąd {response.status_code}: {response.text}", parent=parent)
            return None

    def korekta_karty_odrzuconej(self, data, parent):
        url = self.url_korekta_karty_odrzuconej
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }

        response = requests.put(url, headers=headers, json=data)

        if response.status_code == 200 or response.status_code == 201:

            data_response = response.json()
            tk.messagebox.showinfo("Sukces", "Dokonano korekcji odrzuconej karty", parent=parent)
            return data_response
        elif response.status_code == 204:

            tk.messagebox.showinfo("Sukces", "Dokonano korekcji odrzuconej karty", parent=parent)
            return None
        else:

            tk.messagebox.showerror("Błąd", f"Odpowiedź serwera: Błąd {response.status_code}: {response.text}", parent=parent)
            return None

    def zmiana_statusu_karty_z_planowanej_na_zatwierdzona(self, KpoId, parent):
        url = self.url_zmiana_statusu_karty_z_planowanej_na_zatwierdzona
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }

        data = {
            "KpoId": KpoId
        }

        response = requests.put(url, headers=headers, json=data)

        if response.status_code in [204, 201]:

            tk.messagebox.showinfo("Sukces", "Zmieniono status na Zatwierdzona", parent=parent)
            return {}
        else:

            try:
                data = response.json()
                return data
            except ValueError:

                tk.messagebox.showerror("Błąd", f"Odpowiedź serwera: Błąd {response.status_code}: {response.text}", parent=parent)
                return None

    def usuwanie_karty_ze_statusem_planowana(self, KpoId, parent):
        url = self.url_usuwanie_karty_ze_statusem_planowana
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }

        data = {
            "KpoId": KpoId
        }

        response = requests.delete(url, headers=headers, json=data)

        if response.status_code in [204, 201]:
            tk.messagebox.showinfo("Sukces", "Usunięto kartę planowaną", parent=parent)
            return {}
        else:
            try:
                data = response.json()
                return data
            except ValueError:
                tk.messagebox.showerror("Błąd", f"Odpowiedź serwera: Błąd {response.status_code}: {response.text}", parent=parent)
                return None

    def zmiana_statusu_na_wycofana(self,KpoId, Remarks, parent):
        url = self.url_zmiana_statusu_na_wycofana
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }

        data = {
            "KpoId": KpoId,
            "Remarks": Remarks
        }

        response = requests.put(url, headers=headers, json=data)

        if response.status_code in [204, 201]:
            tk.messagebox.showinfo("Sukces", "Zmieniono status na Wycofana", parent=parent)
            return {}
        else:
            try:
                data = response.json()
                return data
            except ValueError:
                tk.messagebox.showerror("Błąd", f"Odpowiedź serwera: Błąd {response.status_code}: {response.text}", parent=parent)
                return None


    def zmiana_statusu_na_odrzucona(self,KpoId, Remarks, parent):
        url = self.url_zmiana_statusu_na_odrzucona
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }

        data = {
            "KpoId": KpoId,
            "Remarks": Remarks
        }

        response = requests.put(url, headers=headers, json=data)

        if response.status_code in [204, 201]:
            tk.messagebox.showinfo("Sukces", "Zmieniono status na Odrzucona", parent=parent)
            return {}
        else:
            tk.messagebox.showerror("Błąd", f"Upewnij się, że masz prawo do tej karty", parent=parent)
            try:
                data = response.json()
                return data
            except ValueError:
                tk.messagebox.showerror("Błąd", f"Odpowiedź serwera: Błąd {response.status_code}: {response.text}", parent=parent)
                return None

    def Zmiana_statusu_karty_z_wygenerowane_potwierdzenie_na_potwierdzenie_przyjecia(self, KpoId, CorrectMass, Remarks, parent):
        url = self.url_zmiana_statusu_karty_z_wygenerowane_potwierdzenie_na_potwierdzenie_przyjecia
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }

        data = {
            "KpoId": KpoId,
            "CorrectedWasteMass": CorrectMass,
            "Remarks": Remarks
        }

        response = requests.put(url, headers=headers, json=data)

        if response.status_code in [204, 200]:
            messagebox.showinfo("Sukces", "Zmieniono status na Potwierdzenie Przyjęcia", parent=parent)
            return {}
        else:

            messagebox.showerror("Błąd", f"Odpowiedź serwera: Błąd {response.status_code}: {response.text}", parent=parent)
            return None


    def wygenerowanie_potwierdzenia_gdzie_podmiot_jest_transportujacy(self, KpoId, VehNumber, RealTransportTime,
                                                                      RealTransportDate, parent):
        url = self.url_wygenerowanie_potwierdzenia_gdzie_podmiot_jest_transportujacy
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }

        data = {
            "KpoId": KpoId,
            "VehicleRegNumber": VehNumber,
            "RealTransportTime": RealTransportTime,
            "RealTransportDate": RealTransportDate
        }

        response = requests.put(url, headers=headers, json=data)

        if response.status_code in [204, 205, 202, 200, 201]:
            tk.messagebox.showinfo("Sukces", "Zmieniono status na Potwierdzony Transport", parent=parent)
            return {}
        else:
            error_message = f"Odpowiedź serwera: Błąd {response.status_code}"
            try:
                data = response.json()

                if isinstance(data, dict):
                    detailed_error = data.get('message', str(data))
                    error_message += f": {detailed_error}"
                else:

                    error_message += f": {data}"
            except ValueError:

                error_message += f": {response.text}"

            tk.messagebox.showerror("Błąd", error_message, parent=parent)
            return None


    def wygenerowanie_potwierdzenia_gdzie_podmiot_jest_przekazujacy(self,data,parent):
        url = self.url_wygenerowanie_potwierdzenia_gdzie_podmiot_jest_przekazujacy

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }

        response = requests.put(url, headers=headers, json=data)

        if response.status_code in [204, 201]:

            tk.messagebox.showinfo("Sukces", "Zmieniono status na Potwierdzony Transport", parent=parent)
            return {}
        else:
            try:
                data = response.json()
                return data
            except ValueError:
                tk.messagebox.showerror("Błąd", f"Odpowiedź serwera: Błąd {response.status_code}: {response.text}", parent=parent)
                return None

    def wygeneruj_potwierdzenie(self, KpoId, VehNumber, RealTransportTime, RealTransportDate, data2, parent):
        url_transportujacy = self.url_wygenerowanie_potwierdzenia_gdzie_podmiot_jest_transportujacy
        url_przekazujacy = self.url_wygenerowanie_potwierdzenia_gdzie_podmiot_jest_przekazujacy

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }

        data = {
            "KpoId": KpoId,
            "VehicleRegNumber": VehNumber,
            "RealTransportTime": RealTransportTime,
            "RealTransportDate": RealTransportDate
        }

        response = requests.put(url_transportujacy, headers=headers, json=data)
        if response.status_code in [200, 201, 202, 204, 205]:
            tk.messagebox.showinfo("Sukces", "Zmieniono status na Potwierdzony Transport (transportujący)", parent=parent)
            return True
        else:

            response = requests.put(url_przekazujacy, headers=headers, json=data2)
            if response.status_code in [200, 201, 204]:
                tk.messagebox.showinfo("Sukces", "Zmieniono status na Potwierdzony Transport (przekazujący)", parent=parent)
                return True
            else:
                tk.messagebox.showerror("Błąd", f"Nie udało się zmienić statusu: {response.text}", parent=parent)
                return False

    def lista_kart_ze_statusem_zrealizowane_przejecie_lub_potwierdzony_transport_dla_przekazujacego(self):
        url = self.url_lista_kart_ze_statusem_zrealizowane_przejecie_lub_potwierdzony_transport_dla_przekazujacego
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }


        params = {
            "PageSize": 10,
            "PaginationParameters.Order.IsAscending": False,
            "PaginationParameters.Order.OrderColumn": "cardNumber",
            "PaginationParameters.Page.Index": 1,
            "PaginationParameters.Page.Size": 50,
            "PaginationParameters.GetOrderColumn": None,
            "PaginationParameters.GetOrderDirection": "DESC",
            "PaginationParameters.GetOrdering": None,
            "ReceiverIdentificationNumber": None,
            "ReceiverName": None,
            "ReceiverNip": None,
            "CardNumber": None,
            "ReceiveConfirmationTime": None,
            "CardStatusCodeNames": None,
            "WasteCodeName": None,
            "IsUsed": False
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:

            data = response.json()
            return data
        elif response.status_code == 201:

            data = response.json()
            return data
        else:
            return None

    def lista_kart_ze_statusem_zrealizowane_przejecie_lub_potwierdzony_transport_dla_przejmujacego(self):
        url = self.url_lista_kart_ze_statusem_zrealizowane_przejecie
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }


        params = {
            "PageSize": 10,
            "PaginationParameters.Order.IsAscending": False,
            "PaginationParameters.Order.OrderColumn": "cardNumber",
            "PaginationParameters.Page.Index": 1,
            "PaginationParameters.Page.Size": 50,
            "PaginationParameters.GetOrderColumn": None,
            "PaginationParameters.GetOrderDirection": "DESC",
            "PaginationParameters.GetOrdering": None,
            "ReceiverIdentificationNumber": None,
            "ReceiverName": None,
            "ReceiverNip": None,
            "CardNumber": None,
            "ReceiveConfirmationTime": None,
            "CardStatusCodeNames": None,
            "WasteCodeName": None,
            "IsUsed": False
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:

            data = response.json()
            return data
        elif response.status_code == 201:

            data = response.json()
            return data
        else:
            return None

    def zmiana_statusu_karty_na_potwierdzenie_wygenerowane(self,KpoId, parent):
        url = self.url_zmiana_statusu_karty_na_potwierdzenie_wygenerowane

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }

        data = {
            "KpoId": KpoId
        }

        response = requests.put(url, headers=headers, json=data)

        if response.status_code in [204, 201]:

            tk.messagebox.showinfo("Sukces", "Zmieniono status na Potwierdzenie wygenerowane", parent=parent)
            return {}
        else:
            try:
                data = response.json()
                return data
            except ValueError:
                tk.messagebox.showerror("Błąd", f"Odpowiedź serwera: Błąd {response.status_code}: {response.text}", parent=parent)
                return None

    def pobieranie_danych_do_wydruku(self,KpoId):
        url = self.url_pobieranie_danych_do_wydruku
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }

        params = {
            "KpoId": KpoId,
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:

            data = response.json()
            print(data)
            return data
        else:

            data = (f"Błąd {response.status_code}: {response.text}")
            print(data)
            return data

    def wydruk(self, KpoId, FilePathWithName):
        url = self.url_wydruk
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }

        params = {
            "KpoId": KpoId,
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:

            data = response.json()
            decoded_pdf = base64.b64decode(data)

            with open(FilePathWithName, "wb") as pdf_file:
                pdf_file.write(decoded_pdf)

            return data
        else:

            data = (f"Błąd {response.status_code}: {response.text}")
            return data

    def wydruk_karty(self, KpoId, FilePathWithName):
        url = self.url_wydruk_karty
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }

        params = {
            "KpoId": KpoId,
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:

            data = response.json()
            decoded_pdf = base64.b64decode(data)

            with open(FilePathWithName, "wb") as pdf_file:
                pdf_file.write(decoded_pdf)

            return data
        else:

            data = (f"Błąd {response.status_code}: {response.text}")
            return data

    def zmiana_statusus_na_potwierdzenie_transportu(self, KpoId, parent):
        url = self.url_zmiana_statusus_na_potwierdzenie_transportu

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }

        data = {
            "KpoId": KpoId
        }

        response = requests.put(url, headers=headers, json=data)

        if response.status_code in [204, 200, 201]:

            tk.messagebox.showinfo("Sukces", "Zmieniono status na Potwierdzony Transport", parent=parent)
            return {}
        else:
            try:
                tk.messagebox.showerror("Błąd","Wystąpił błąd", parent=parent)
                data = response.json()
                return data
            except ValueError:
                tk.messagebox.showerror("Błąd", f"Odpowiedź serwera: Błąd {response.status_code}: {response.text}", parent=parent)
                return None

class Search:
    def __init__(self):
        self.jwt_token_tuple = ApiConnection.GetToken.read_access_token_from_csv()
        self.jwt_token = self.jwt_token_tuple['AccessToken']
        urls = select_version(state)

        self.url_lista_kart_ze_statusem_zrealizowane_przejecie = urls['url_lista_kart_ze_statusem_zrealizowane_przejecie']
        self.url_szczegoly_karty_planowana = urls['url_szczegoly_karty_planowana']
        self.url_szczegoly_karty_wycofana = urls['url_szczegoly_karty_wycofana']
        self.url_szczegoly_karty_zatwierdzona = urls['url_szczegoly_karty_zatwierdzona']
        self.url_szczegoly_karty_wygenerowane_potwierdzenie = urls['url_szczegoly_karty_wygenerowane_potwierdzenie']
        self.url_szczegoly_karty_wygenerowane_potwierdzone_przyjecie = urls['url_szczegoly_karty_wygenerowane_potwierdzone_przyjecie']
        self.url_szczegoly_karty_odrzucona = urls['url_szczegoly_karty_odrzucona']
        self.url_szczegoly_karty_potwierdzony_transport = urls['url_szczegoly_karty_potwierdzony_transport']
        self.url_tworzenie_karty_ze_statusem_planowana = urls['url_tworzenie_karty_ze_statusem_planowana']
        self.url_wyszukiwarka_kart = urls['url_wyszukiwarka_kart']
        self.url_wyszukiwarka_kart_transportujacy = urls['url_wyszukiwarka_kart_transportujacy']
        self.url_wyszukiwarka_kart_przejmujacy = urls['url_wyszukiwarka_kart_przejmujacy']
        self.url_edycja_karty_ze_statusem_planowana = urls['url_edycja_karty_ze_statusem_planowana']
        self.url_edycja_karty_ze_statusem_zatwierdzona = urls['url_edycja_karty_ze_statusem_zatwierdzona']
        self.url_korekta_karty_odrzuconej = urls['url_korekta_karty_odrzuconej']
        self.url_zmiana_statusu_karty_z_planowanej_na_zatwierdzona = urls['url_zmiana_statusu_karty_z_planowanej_na_zatwierdzona']
        self.url_usuwanie_karty_ze_statusem_planowana = urls['url_usuwanie_karty_ze_statusem_planowana']
        self.url_zmiana_statusu_na_wycofana = urls['url_zmiana_statusu_na_wycofana']
        self.url_zmiana_statusu_na_odrzucona = urls['url_zmiana_statusu_na_odrzucona']
        self.url_zmiana_statusu_karty_z_wygenerowane_potwierdzenie_na_potwierdzenie_przyjecia = urls['url_zmiana_statusu_karty_z_wygenerowane_potwierdzenie_na_potwierdzenie_przyjecia']
        self.url_wygenerowanie_potwierdzenia_gdzie_podmiot_jest_transportujacy = urls['url_wygenerowanie_potwierdzenia_gdzie_podmiot_jest_transportujacy']
        self.url_wygenerowanie_potwierdzenia_gdzie_podmiot_jest_przekazujacy = urls['url_wygenerowanie_potwierdzenia_gdzie_podmiot_jest_przekazujacy']
        self.url_lista_kart_ze_statusem_zrealizowane_przejecie_lub_potwierdzony_transport_dla_przekazujacego = urls['url_lista_kart_ze_statusem_zrealizowane_przejecie_lub_potwierdzony_transport_dla_przekazujacego']
        self.url_zmiana_statusu_karty_na_potwierdzenie_wygenerowane = urls['url_zmiana_statusu_karty_na_potwierdzenie_wygenerowane']
        self.url_pobieranie_danych_do_wydruku = urls['url_pobieranie_danych_do_wydruku']
        self.url_wydruk = urls['url_wydruk']
        self.url_wydruk_karty = urls['url_wydruk_karty']
        self.url_zmiana_statusus_na_potwierdzenie_transportu = urls['url_zmiana_statusus_na_potwierdzenie_transportu']
        self.url_zwraca_liste_rekordow_zgodnie_z_wartoscia_zapytania = urls['url_zwraca_liste_rekordow_zgodnie_z_wartoscia_zapytania']
        self.url_wyszukiwarka_po_copmany_id = urls['url_wyszukiwarka_po_copmany_id']
        self.url_wyszukiwarka_dane_miejsca_po_eup_id = urls['url_wyszukiwarka_dane_miejsca_po_eup_id']
        self.url_zwroc_10_rekorwow_z_danymi_miejsc_prowadzenia_dzialanosci = urls['url_zwroc_10_rekorwow_z_danymi_miejsc_prowadzenia_dzialanosci']
        self.url_zwraca_liste_gmin = urls['url_zwraca_liste_gmin']
        self.url_zwraca_liste_gmin_po_id = urls['url_zwraca_liste_gmin_po_id']

    def ZwracaListeRekordowZgodniezwartosciazapytania(self,query):
        url = self.url_zwraca_liste_rekordow_zgodnie_z_wartoscia_zapytania
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }

        params = {
            "Query": query,
        }

        response = requests.get(url, headers=headers,params=params)

        if response.status_code == 200:

            data = response.json()
            print(data)
            return data
        else:

            data = (f"Błąd {response.status_code}: {response.text}")
            print(data)
            return data

    def WyszukiwarkaPoCopmanyID(self, company_id):
        url = self.url_wyszukiwarka_po_copmany_id

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }

        params = {
            "companyId": company_id,
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:

            data = response.json()
            print(data)
            return data
        else:

            data = (f"Błąd {response.status_code}: {response.text}")
            print(data)
            return data

    def WyszukiwarkaDaneMiejscaPoEUPID(self, eupId):
        url = self.url_wyszukiwarka_dane_miejsca_po_eup_id
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }

        params = {
            "eupId": eupId,
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:

            data = response.json()
            print(data)
            return data
        else:

            data = (f"Błąd {response.status_code}: {response.text}")
            print(data)
            return data

    def Zwroc10rekorwowzdanymimiejscprowadzeniadzialanosci(self, company_id):
        url = self.url_zwroc_10_rekorwow_z_danymi_miejsc_prowadzenia_dzialanosci

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }

        params = {
            "companyId": company_id,
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:

            data = response.json()
            print(data)
            return data
        else:

            data = (f"Błąd {response.status_code}: {response.text}")
            print(data)
            return data

    def ZwracaListeGmin(self, query):
        url = self.url_zwraca_liste_gmin

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }

        params = {
            "Query": query,
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:

            data = response.json()
            print(data)
            return data
        else:

            data = (f"Błąd {response.status_code}: {response.text}")
            print(data)
            return data

    def ZwracaListeGminPoId(self, query):
        url = self.url_zwraca_liste_gmin_po_id

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        }

        params = {
            "Query": query,
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:

            data = response.json()
            print(data)
            return data
        else:

            data = (f"Błąd {response.status_code}: {response.text}")
            print(data)
            return data


if __name__ == "__main__":
    KPO().wyszukiwarka_kart_transportujacy(1, 50, False)