import csv
import os


state = "test"


""" Ścieżka do pliku CSV z konfiguracją bazy danych """
file_path = 'temp/db_config3.csv'

""" Ścieżka do pliku CSV z danymi kart przekazującego """
csv_transporter_file = 'temp/12TEST.csv'

""" Ścieżka do pliku CSV z danymi kart transportującego """
csv_receiver_file = 'temp/14TEST.csv'

""" Ścieżka do pliku CSV z danymi kart odbierającego """
csv_transmitter_file = 'temp/11TEST.csv'

""" Kolor obwódki frame """
highlightcolor = "#0063b1"

""" Kolor tła frame """
highlightbackground = "#DCDCDC"

""" Ścieżka do pliku CSV z ClienId, ClientSecret i EupID"""
credentials_csv_path = 'temp/Credentials_data.csv'

""" Ścieżka do pliku CSV z miejscem oraz danymi miejsca prowadzenia działalności (wybór wg indeksu)"""
access_data_csv_path = 'temp/Access_data.csv'

""" Ścieżka do pliku CSV z danymi tokena """
token_data_csv_path = 'temp/Token_data.csv'


def create_csv_if_not_exists():
    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)




            writer.writerow(['host', '127.0.0.1'])
            writer.writerow(['user', 'root'])
            writer.writerow(['password', None])  # Wstaw swoje hasło
            writer.writerow(['database', 'twojabazadanych'])

def load_db_config():
    config = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:
                    config[row[0]] = row[1]
        return config
    except FileNotFoundError:
        print("Plik CSV nie został znaleziony.")
        return None

def read_second_value_from_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            return row['pageNumber']

def select_version(version):
    if version == "test":
        url_show_access_attempt_with_auth = "https://test-bdo.mos.gov.pl/api/WasteRegister/v1/Auth/getEupList"
        url_access_attempt_with_auth = "https://test-bdo.mos.gov.pl/api/WasteRegister/v1/Auth/getEupList"
        url_authenticate_with_credentials ="https://test-bdo.mos.gov.pl/api/WasteRegister/v1/Auth/generateEupAccessToken"
        url_lista_kart_ze_statusem_zrealizowane_przejecie = "https://test-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/sendercards/receiver"
        url_szczegoly_karty_planowana = 'https://test-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/planned/card'
        url_szczegoly_karty_wycofana = 'https://test-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/withdrawn/card'
        url_szczegoly_karty_zatwierdzona = 'https://test-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/approved/card'
        url_szczegoly_karty_wygenerowane_potwierdzenie = 'https://test-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/confirmationgenerated/card'
        url_szczegoly_karty_wygenerowane_potwierdzone_przyjecie = 'https://test-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/receiveconfirmed/card'
        url_szczegoly_karty_odrzucona = 'https://test-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/rejected/card'
        url_szczegoly_karty_potwierdzony_transport = 'https://test-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/transportconfirmation/card'
        url_tworzenie_karty_ze_statusem_planowana = 'https://test-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/create/plannedcard'
        url_wyszukiwarka_kart = 'https://test-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/sender/search'
        url_wyszukiwarka_kart_transportujacy = 'https://test-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/carrier/search'
        url_wyszukiwarka_kart_przejmujacy = 'https://test-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/receiver/search'
        url_edycja_karty_ze_statusem_planowana = 'https://test-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/update/plannedcard'
        url_edycja_karty_ze_statusem_zatwierdzona = 'https://test-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/update/approvedcard'
        url_korekta_karty_odrzuconej = 'https://test-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/revise'
        url_zmiana_statusu_karty_z_planowanej_na_zatwierdzona = 'https://test-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/approve'
        url_usuwanie_karty_ze_statusem_planowana = 'https://test-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/delete'
        url_zmiana_statusu_na_wycofana = 'https://test-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/withdrawn'
        url_zmiana_statusu_na_odrzucona = 'https://test-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/reject'
        url_zmiana_statusu_karty_z_wygenerowane_potwierdzenie_na_potwierdzenie_przyjecia = 'https://test-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/assign/receiveconfirmation'
        url_wygenerowanie_potwierdzenia_gdzie_podmiot_jest_transportujacy = 'https://test-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/carrier/update/approved/generateconfirmation'
        url_wygenerowanie_potwierdzenia_gdzie_podmiot_jest_przekazujacy = 'https://test-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/sender/update/approved/generateconfirmation'
        url_lista_kart_ze_statusem_zrealizowane_przejecie_lub_potwierdzony_transport_dla_przekazujacego = 'https://test-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/receivercards/sender'
        url_zmiana_statusu_karty_na_potwierdzenie_wygenerowane = 'https://test-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/generateconfirmation'
        url_pobieranie_danych_do_wydruku = 'https://test-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/printingpage'
        url_wydruk = 'https://test-bdo.mos.gov.pl/api/WasteRegister/DocumentService/v1/kpo/confirmation'
        url_wydruk_karty = 'https://test-bdo.mos.gov.pl/api/WasteRegister/DocumentService/v1/kpo/printingpage'
        url_zmiana_statusus_na_potwierdzenie_transportu = 'https://test-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/status/transportconfirmation'
        url_zwraca_liste_rekordow_zgodnie_z_wartoscia_zapytania = 'https://test-bdo.mos.gov.pl/api/WasteRegister/v1/Search/searchcompany'
        url_wyszukiwarka_po_copmany_id = 'https://test-bdo.mos.gov.pl/api/WasteRegister/v1/Search/getcompanybyid'
        url_wyszukiwarka_dane_miejsca_po_eup_id = 'https://test-bdo.mos.gov.pl/api/WasteRegister/v1/Search/geteupbyid'
        url_zwroc_10_rekorwow_z_danymi_miejsc_prowadzenia_dzialanosci = 'https://test-bdo.mos.gov.pl/api/WasteRegister/v1/Search/geteupsbycompanyid'
        url_zwraca_liste_gmin = 'https://test-bdo.mos.gov.pl/api/WasteRegister/v1/Search/searchterytcommune'
        url_zwraca_liste_gmin_po_id = 'https://test-bdo.mos.gov.pl/api/WasteRegister/v1/Search/getterytcommunebyid'
        url_zwraca_kod_odpadu = "https://test-bdo.mos.gov.pl/api/WasteRegister/v1/WasteCode"
        url_szuka_kod_odpadu = "https://test-bdo.mos.gov.pl/api/WasteRegister/v1/WasteCode/search"
        url_zwraca_proces_odpadu = "https://test-bdo.mos.gov.pl/api/WasteRegister/v1/WasteProcess"
        url_szuka_proces_odpadu = "https://test-bdo.mos.gov.pl/api/WasteRegister/v1/WasteProcess/search"


        urls = {
            "url_show_access_attempt_with_auth": url_show_access_attempt_with_auth,
            "url_access_attempt_with_auth": url_access_attempt_with_auth,
            "url_authenticate_with_credentials": url_authenticate_with_credentials,
            "url_lista_kart_ze_statusem_zrealizowane_przejecie": url_lista_kart_ze_statusem_zrealizowane_przejecie,
            "url_szczegoly_karty_planowana": url_szczegoly_karty_planowana,
            "url_szczegoly_karty_wycofana": url_szczegoly_karty_wycofana,
            "url_szczegoly_karty_zatwierdzona": url_szczegoly_karty_zatwierdzona,
            "url_szczegoly_karty_wygenerowane_potwierdzenie": url_szczegoly_karty_wygenerowane_potwierdzenie,
            "url_szczegoly_karty_wygenerowane_potwierdzone_przyjecie": url_szczegoly_karty_wygenerowane_potwierdzone_przyjecie,
            "url_szczegoly_karty_odrzucona": url_szczegoly_karty_odrzucona,
            "url_szczegoly_karty_potwierdzony_transport": url_szczegoly_karty_potwierdzony_transport,
            "url_tworzenie_karty_ze_statusem_planowana": url_tworzenie_karty_ze_statusem_planowana,
            "url_wyszukiwarka_kart": url_wyszukiwarka_kart,
            "url_wyszukiwarka_kart_transportujacy": url_wyszukiwarka_kart_transportujacy,
            "url_wyszukiwarka_kart_przejmujacy": url_wyszukiwarka_kart_przejmujacy,
            "url_edycja_karty_ze_statusem_planowana": url_edycja_karty_ze_statusem_planowana,
            "url_edycja_karty_ze_statusem_zatwierdzona": url_edycja_karty_ze_statusem_zatwierdzona,
            "url_korekta_karty_odrzuconej": url_korekta_karty_odrzuconej,
            "url_zmiana_statusu_karty_z_planowanej_na_zatwierdzona": url_zmiana_statusu_karty_z_planowanej_na_zatwierdzona,
            "url_usuwanie_karty_ze_statusem_planowana": url_usuwanie_karty_ze_statusem_planowana,
            "url_zmiana_statusu_na_wycofana": url_zmiana_statusu_na_wycofana,
            "url_zmiana_statusu_na_odrzucona": url_zmiana_statusu_na_odrzucona,
            "url_zmiana_statusu_karty_z_wygenerowane_potwierdzenie_na_potwierdzenie_przyjecia": url_zmiana_statusu_karty_z_wygenerowane_potwierdzenie_na_potwierdzenie_przyjecia,
            "url_wygenerowanie_potwierdzenia_gdzie_podmiot_jest_transportujacy": url_wygenerowanie_potwierdzenia_gdzie_podmiot_jest_transportujacy,
            "url_wygenerowanie_potwierdzenia_gdzie_podmiot_jest_przekazujacy": url_wygenerowanie_potwierdzenia_gdzie_podmiot_jest_przekazujacy,
            "url_lista_kart_ze_statusem_zrealizowane_przejecie_lub_potwierdzony_transport_dla_przekazujacego": url_lista_kart_ze_statusem_zrealizowane_przejecie_lub_potwierdzony_transport_dla_przekazujacego,
            "url_zmiana_statusu_karty_na_potwierdzenie_wygenerowane": url_zmiana_statusu_karty_na_potwierdzenie_wygenerowane,
            "url_pobieranie_danych_do_wydruku": url_pobieranie_danych_do_wydruku,
            "url_wydruk": url_wydruk,
            "url_wydruk_karty": url_wydruk_karty,
            "url_zmiana_statusus_na_potwierdzenie_transportu": url_zmiana_statusus_na_potwierdzenie_transportu,
            "url_zwraca_liste_rekordow_zgodnie_z_wartoscia_zapytania": url_zwraca_liste_rekordow_zgodnie_z_wartoscia_zapytania,
            "url_wyszukiwarka_po_copmany_id": url_wyszukiwarka_po_copmany_id,
            "url_wyszukiwarka_dane_miejsca_po_eup_id": url_wyszukiwarka_dane_miejsca_po_eup_id,
            "url_zwroc_10_rekorwow_z_danymi_miejsc_prowadzenia_dzialanosci": url_zwroc_10_rekorwow_z_danymi_miejsc_prowadzenia_dzialanosci,
            "url_zwraca_liste_gmin": url_zwraca_liste_gmin,
            "url_zwraca_liste_gmin_po_id": url_zwraca_liste_gmin_po_id,
            "url_zwraca_kod_odpadu" : url_zwraca_kod_odpadu,
            "url_szuka_kod_odpadu": url_szuka_kod_odpadu,
            "url_zwraca_proces_odpadu" : url_zwraca_proces_odpadu,
            "url_szuka_proces_odpadu": url_szuka_proces_odpadu

        }
        return urls

    elif version == "official":
        url_show_access_attempt_with_auth = "https://rejestr-bdo.mos.gov.pl/api/WasteRegister/v1/Auth/getEupList"
        url_access_attempt_with_auth = "https://rejestr-bdo.mos.gov.pl/api/WasteRegister/v1/Auth/getEupList"
        url_authenticate_with_credentials = "https://rejestr-bdo.mos.gov.pl/api/WasteRegister/v1/Auth/generateEupAccessToken"
        url_lista_kart_ze_statusem_zrealizowane_przejecie = "https://rejestr-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/sendercards/receiver"
        url_szczegoly_karty_planowana = 'https://rejestr-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/planned/card'
        url_szczegoly_karty_wycofana = 'https://rejestr-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/withdrawn/card'
        url_szczegoly_karty_zatwierdzona = 'https://rejestr-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/approved/card'
        url_szczegoly_karty_wygenerowane_potwierdzenie = 'https://rejestr-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/confirmationgenerated/card'
        url_szczegoly_karty_wygenerowane_potwierdzone_przyjecie = 'https://rejestr-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/receiveconfirmed/card'
        url_szczegoly_karty_odrzucona = 'https://rejestr-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/rejected/card'
        url_szczegoly_karty_potwierdzony_transport = 'https://rejestr-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/transportconfirmation/card'
        url_tworzenie_karty_ze_statusem_planowana = 'https://rejestr-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/create/plannedcard'
        url_wyszukiwarka_kart = 'https://rejestr-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/sender/search'
        url_wyszukiwarka_kart_transportujacy = 'https://rejestr-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/carrier/search'
        url_wyszukiwarka_kart_przejmujacy = 'https://rejestr-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/receiver/search'
        url_edycja_karty_ze_statusem_planowana = 'https://rejestr-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/update/plannedcard'
        url_edycja_karty_ze_statusem_zatwierdzona = 'https://rejestr-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/update/approvedcard'
        url_korekta_karty_odrzuconej = 'https://rejestr-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/revise'
        url_zmiana_statusu_karty_z_planowanej_na_zatwierdzona = 'https://rejestr-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/approve'
        url_usuwanie_karty_ze_statusem_planowana = 'https://rejestr-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/delete'
        url_zmiana_statusu_na_wycofana = 'https://rejestr-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/withdrawn'
        url_zmiana_statusu_na_odrzucona = 'https://rejestr-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/reject'
        url_zmiana_statusu_karty_z_wygenerowane_potwierdzenie_na_potwierdzenie_przyjecia = 'https://rejestr-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/assign/receiveconfirmation'
        url_wygenerowanie_potwierdzenia_gdzie_podmiot_jest_transportujacy = 'https://rejestr-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/carrier/update/approved/generateconfirmation'
        url_wygenerowanie_potwierdzenia_gdzie_podmiot_jest_przekazujacy = 'https://rejestr-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/sender/update/approved/generateconfirmation'
        url_lista_kart_ze_statusem_zrealizowane_przejecie_lub_potwierdzony_transport_dla_przekazujacego = 'https://rejestr-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/receivercards/sender'
        url_zmiana_statusu_karty_na_potwierdzenie_wygenerowane = 'https://rejestr-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/generateconfirmation'
        url_pobieranie_danych_do_wydruku = 'https://rejestr-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/printingpage'
        url_wydruk = 'https://rejestr-bdo.mos.gov.pl/api/WasteRegister/DocumentService/v1/kpo/confirmation'
        url_wydruk_karty = 'https://rejestr-bdo.mos.gov.pl/api/WasteRegister/DocumentService/v1/kpo/printingpage'
        url_zmiana_statusus_na_potwierdzenie_transportu = 'https://rejestr-bdo.mos.gov.pl/api/WasteRegister/WasteTransferCard/v1/Kpo/status/transportconfirmation'
        url_zwraca_liste_rekordow_zgodnie_z_wartoscia_zapytania = 'https://rejestr-bdo.mos.gov.pl/api/WasteRegister/v1/Search/searchcompany'
        url_wyszukiwarka_po_copmany_id = 'https://rejestr-bdo.mos.gov.pl/api/WasteRegister/v1/Search/getcompanybyid'
        url_wyszukiwarka_dane_miejsca_po_eup_id = 'https://rejestr-bdo.mos.gov.pl/api/WasteRegister/v1/Search/geteupbyid'
        url_zwroc_10_rekorwow_z_danymi_miejsc_prowadzenia_dzialanosci = 'https://rejestr-bdo.mos.gov.pl/api/WasteRegister/v1/Search/geteupsbycompanyid'
        url_zwraca_liste_gmin = 'https://rejestr-bdo.mos.gov.pl/api/WasteRegister/v1/Search/searchterytcommune'
        url_zwraca_liste_gmin_po_id = 'https://rejestr-bdo.mos.gov.pl/api/WasteRegister/v1/Search/getterytcommunebyid'
        url_zwraca_kod_odpadu = "https://rejestr-bdo.mos.gov.pl/api/WasteRegister/v1/WasteCode"
        url_szuka_kod_odpadu = "https://rejestr-bdo.mos.gov.pl/api/WasteRegister/v1/WasteCode/search"
        url_zwraca_proces_odpadu = "https://rejestr-bdo.mos.gov.pl/api/WasteRegister/v1/WasteProcess"
        url_szuka_proces_odpadu = "https://rejestr-bdo.mos.gov.pl/api/WasteRegister/v1/WasteProcess/search"

        urls = {
            "url_show_access_attempt_with_auth": url_show_access_attempt_with_auth,
            "url_access_attempt_with_auth": url_access_attempt_with_auth,
            "url_authenticate_with_credentials": url_authenticate_with_credentials,
            "url_lista_kart_ze_statusem_zrealizowane_przejecie": url_lista_kart_ze_statusem_zrealizowane_przejecie,
            "url_szczegoly_karty_planowana": url_szczegoly_karty_planowana,
            "url_szczegoly_karty_wycofana": url_szczegoly_karty_wycofana,
            "url_szczegoly_karty_zatwierdzona": url_szczegoly_karty_zatwierdzona,
            "url_szczegoly_karty_wygenerowane_potwierdzenie": url_szczegoly_karty_wygenerowane_potwierdzenie,
            "url_szczegoly_karty_wygenerowane_potwierdzone_przyjecie": url_szczegoly_karty_wygenerowane_potwierdzone_przyjecie,
            "url_szczegoly_karty_odrzucona": url_szczegoly_karty_odrzucona,
            "url_szczegoly_karty_potwierdzony_transport": url_szczegoly_karty_potwierdzony_transport,
            "url_tworzenie_karty_ze_statusem_planowana": url_tworzenie_karty_ze_statusem_planowana,
            "url_wyszukiwarka_kart": url_wyszukiwarka_kart,
            "url_wyszukiwarka_kart_transportujacy": url_wyszukiwarka_kart_transportujacy,
            "url_wyszukiwarka_kart_przejmujacy": url_wyszukiwarka_kart_przejmujacy,
            "url_edycja_karty_ze_statusem_planowana": url_edycja_karty_ze_statusem_planowana,
            "url_edycja_karty_ze_statusem_zatwierdzona": url_edycja_karty_ze_statusem_zatwierdzona,
            "url_korekta_karty_odrzuconej": url_korekta_karty_odrzuconej,
            "url_zmiana_statusu_karty_z_planowanej_na_zatwierdzona": url_zmiana_statusu_karty_z_planowanej_na_zatwierdzona,
            "url_usuwanie_karty_ze_statusem_planowana": url_usuwanie_karty_ze_statusem_planowana,
            "url_zmiana_statusu_na_wycofana": url_zmiana_statusu_na_wycofana,
            "url_zmiana_statusu_na_odrzucona": url_zmiana_statusu_na_odrzucona,
            "url_zmiana_statusu_karty_z_wygenerowane_potwierdzenie_na_potwierdzenie_przyjecia": url_zmiana_statusu_karty_z_wygenerowane_potwierdzenie_na_potwierdzenie_przyjecia,
            "url_wygenerowanie_potwierdzenia_gdzie_podmiot_jest_transportujacy": url_wygenerowanie_potwierdzenia_gdzie_podmiot_jest_transportujacy,
            "url_wygenerowanie_potwierdzenia_gdzie_podmiot_jest_przekazujacy": url_wygenerowanie_potwierdzenia_gdzie_podmiot_jest_przekazujacy,
            "url_lista_kart_ze_statusem_zrealizowane_przejecie_lub_potwierdzony_transport_dla_przekazujacego": url_lista_kart_ze_statusem_zrealizowane_przejecie_lub_potwierdzony_transport_dla_przekazujacego,
            "url_zmiana_statusu_karty_na_potwierdzenie_wygenerowane": url_zmiana_statusu_karty_na_potwierdzenie_wygenerowane,
            "url_pobieranie_danych_do_wydruku": url_pobieranie_danych_do_wydruku,
            "url_wydruk": url_wydruk,
            "url_wydruk_karty": url_wydruk_karty,
            "url_zmiana_statusus_na_potwierdzenie_transportu": url_zmiana_statusus_na_potwierdzenie_transportu,
            "url_zwraca_liste_rekordow_zgodnie_z_wartoscia_zapytania": url_zwraca_liste_rekordow_zgodnie_z_wartoscia_zapytania,
            "url_wyszukiwarka_po_copmany_id": url_wyszukiwarka_po_copmany_id,
            "url_wyszukiwarka_dane_miejsca_po_eup_id": url_wyszukiwarka_dane_miejsca_po_eup_id,
            "url_zwroc_10_rekorwow_z_danymi_miejsc_prowadzenia_dzialanosci": url_zwroc_10_rekorwow_z_danymi_miejsc_prowadzenia_dzialanosci,
            "url_zwraca_liste_gmin": url_zwraca_liste_gmin,
            "url_zwraca_liste_gmin_po_id": url_zwraca_liste_gmin_po_id,
            "url_zwraca_kod_odpadu": url_zwraca_kod_odpadu,
            "url_szuka_kod_odpadu" : url_szuka_kod_odpadu,
            "url_zwraca_proces_odpadu": url_zwraca_proces_odpadu,
            "url_szuka_proces_odpadu" : url_szuka_proces_odpadu
        }
        return urls
    else:
        print("Błąd, aby zadeklarować wersję wpisz 'test' lub 'official'")

create_csv_if_not_exists()
db_config = load_db_config()