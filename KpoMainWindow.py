import tkinter as tk
from tkinter import ttk, messagebox
from TransmitterCards import ReceiveConfirmationCardList, RejectedCardList, TransportConfirmationCardList, PlannedCardList, WithdrawnCardList,ApprovedCardList,ConfirmationGeneratedCardList
import AllCardsAsReceiver
import SelectTransporterWindow
import SelectWasteWindow, WasteProcessWindow
from tkcalendar import Calendar
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import KpoRequests
from Globals import db_config
import mysql.connector
from HistoryCardWinodw import DatabaseApp
import DetalisPlanCard
import LocationSelection
import ApiConnection
import BothStructure
import CompanyLabel
import MainTransmitterWindow
import AllCardsAsTransporter
import WasteCopy
from Globals import highlightcolor, highlightbackground, read_second_value_from_csv, access_data_csv_path, select_version, state
import AllCardsAsTransmitter
import os
import csv
import requests




class StartWindow:
    def __init__(self):
        self.access_data = 'temp/Access_data.csv'
        self.credentials_data = 'temp/Credentials_data.csv'
        self.token_data = 'temp/Token_data.csv'
        self.check_list = [self.access_data, self.credentials_data, self.token_data]
        urls = select_version(state)
        self.url_access_attempt_with_auth = urls['url_access_attempt_with_auth']
        self.url_authenticate_with_credentials = urls['url_authenticate_with_credentials']

    def Error_window(self):
        file = self.check_data()
        conn_test = ApiConnection.Connection().access_attempt_with_auth(1)

        if not file[self.credentials_data] or not file[self.access_data] or not file[self.token_data]:
            self.create_window()
        if not conn_test:
            self.create_window()
        else:
            KPO('Matus').window()


    def create_window(self):
        self.root = tk.Tk()

        frame = tk.Frame(padx=10, pady=5)
        frame.pack()

        self.client_id_entry = ttk.Entry(frame)
        self.client_id_entry.insert(0, "Tu wpisz Client ID")
        self.client_id_entry.grid(row=0, column=0)

        self.client_secret_entry = ttk.Entry(frame)
        self.client_secret_entry.insert(0, "Tu wpisz Client Secret")
        self.client_secret_entry.grid(row=1, column=0)

        self.confirm_button = ttk.Button(frame, text="Potwierdź", command=self.access_attempt_with_auth)
        self.confirm_button.grid(row=2, column=0)

        self.root.mainloop()

    def access_attempt_with_auth(self):
        client_id = self.client_id_entry.get()
        client_secret = self.client_secret_entry.get()

        try:
            endpoint = self.url_access_attempt_with_auth
            auth_data = {
                "ClientId": client_id,
                "ClientSecret": client_secret,
                "PaginationParameters": {
                    "Order": {
                        "IsAscending": True
                    },
                    "Page": {
                        "Index": 0,
                        "Size": 0
                    }
                }
            }

            self.response = requests.post(endpoint, json=auth_data)

            if self.response.status_code == 200:
                data = self.response.json()
                self.save_data_to_csv(data, self.access_data)
                self.save_credentials_to_csv(client_id, client_secret,data, self.credentials_data)
                print("Połączenie z API udane")
                self.root.destroy()
                KPO('Matus').window()
            else:
                tk.messagebox.showerror("Błąd", "Błąd autoryzacji: Błędne dane.")
                print("Połączenie z API nieudane: Status code " + str(self.response.status_code))

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
        self.authenticate_with_credentials(self.credentials_data, self.token_data)

    @staticmethod
    def save_data_to_csv(data, csv_file):
        if os.path.isfile(csv_file):
            os.remove(csv_file)

        with open(csv_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['pageSize', 'pageNumber', 'totalPagesNumber', 'totalResultNumber', 'hasPreviousPage',
                          'hasNextPage', 'eupId', 'companyId', 'name', 'identificationNumber', 'province',
                          'district', 'commune', 'locality', 'street', 'buildingNumber', 'localNumber',
                          'addressHtml', 'isActive']

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            writer.writerow({
                'pageSize': data['pageSize'],
                'pageNumber': data['pageNumber'],
                'totalPagesNumber': data['totalPagesNumber'],
                'totalResultNumber': data['totalResultNumber'],
                'hasPreviousPage': data['hasPreviousPage'],
                'hasNextPage': data['hasNextPage'],
                'eupId': data['items'][0]['eupId'],
                'companyId': data['items'][0]['companyId'],
                'name': data['items'][0]['name'],
                'identificationNumber': data['items'][0]['identificationNumber'],
                'province': data['items'][0]['province'],
                'district': data['items'][0]['district'],
                'commune': data['items'][0]['commune'],
                'locality': data['items'][0]['locality'],
                'street': data['items'][0]['street'],
                'buildingNumber': data['items'][0]['buildingNumber'],
                'localNumber': data['items'][0]['localNumber'],
                'addressHtml': data['items'][0]['addressHtml'],
                'isActive': data['items'][0]['isActive']
            })

    @staticmethod
    def save_credentials_to_csv(client_id, client_secret, data, csv_file):
        eup_id = data['items'][0]['eupId']
        with open(csv_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['Client ID', 'Client Secret', 'eupId']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'Client ID': client_id, 'Client Secret': client_secret, 'eupId':eup_id})

    def load_credentials_from_csv(self, csv_file):
        if os.path.isfile(csv_file):
            with open(csv_file, 'r', newline='', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.default_id = row['Client ID']
                    self.default_secret = row['Client Secret']
                    break

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

    def check_data(self):
        files_dict = {}
        for element in self.check_list:
            result = self.check_temp(element)
            files_dict[element] = result
        return files_dict

    @staticmethod
    def check_temp(file_path):
        if os.path.exists(file_path):
            return True
        else:
            return False

class KPO:

    def __init__(self, user):
        self.creator = user
        self.toplevel = None
        self.waste = SelectWasteWindow.WasteWindow()
        self.waste_list = WasteCopy.WasteCode()
        self.config_data = db_config
        self.host = db_config['host']
        self.user = db_config['user']
        self.password = db_config['password']
        self.database = db_config['database']
        self.DateCorrect = False
        self.process_id = None
        self.default_place = ApiConnection
        self.my_carrier_company_name = '"WODOCIĄGI I KANALIZACJA-ZGIERZ" SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ'
        self.my_carrier_company_id = "c2ea224e-6b5a-4fb3-a246-8e7f76f1c093"
        self.my_receiver_company_name = 'Siedziba: "WODOCIĄGI I KANALIZACJA-ZGIERZ" SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ'
        self.my_receiver_company_id ="c2ea224e-6b5a-4fb3-a246-8e7f76f1c093"
        self.my_receiver_company_eup = "11449732-658f-4de0-8842-2aa31ea047ee"
        self.my_reg_vehicle = "EZG"
        self.my_company = self.default_place.Connection()
        self.planned_card_id = "brak, wybierz kartę"
        self.search_teryt_button_created = False
        self.EditState = None
        self.child_window_transporter = None
        self.child_window_receiver = None
        self.child_window_transmitter = None
        self.company_index = read_second_value_from_csv(access_data_csv_path)
        self.highlightcolor = highlightcolor
        self.highlightbackground = highlightbackground
        self.sticky_n = "n"
        self.highlightthickness = 1
        self.short_button_size = 18
        self.long_button_size = 38


    def history(self):
        self.database_app = DatabaseApp("matus", callback=self.receive_data_from_db_app)
        self.database_app.open_and_fetch_data()


    def receive_data_from_db_app(self, data):
        self.carrier_company_entry.delete(0, tk.END)
        self.carrier_company_entry.insert(0, data[19])
        self.receiver_eup_id_entry.delete(0, tk.END)
        self.receiver_eup_id_entry.insert(0, data[20])
        self.waste_code_id_entry.delete(0, tk.END)
        self.waste_code_id_entry.insert(0, data[21])
        self.waste_process_id_entry.delete(0, tk.END)
        self.waste_process_id_entry.insert(0, data[22])
        self.vehicle_reg_number_entry.delete(0, tk.END)
        self.vehicle_reg_number_entry.insert(0, data[6])
        self.waste_mass_entry.delete(0, tk.END)
        self.waste_mass_entry.insert(0, data[7])
        self.planned_transport_time_entry.delete(0, tk.END)
        self.certificate_number_and_box_numbers_entry.delete(0, tk.END)
        self.certificate_number_and_box_numbers_entry.insert(0, data[10])
        self.additional_info_entry.delete('1.0', tk.END)
        self.additional_info_entry.insert('1.0', data[11])
        self.waste_code_extended_var.set(data[12])

        if data[12] == 1:
            self.waste_code_extended_description_entry['state'] = 'normal'
            self.waste_code_extended_description_entry.config(background="white")
            self.waste_code_extended_description_entry.delete('1.0', tk.END)
            self.waste_code_extended_description_entry.insert('1.0', data[13])

        self.hazardous_waste_reclassification_var.set(data[14])
        if data[14] == 1:
            self.hazardous_waste_reclassification_description_entry['state'] = 'normal'
            self.hazardous_waste_reclassification_description_entry.config(background="white")
            self.hazardous_waste_reclassification_description_entry.delete('1.0', tk.END)
            self.hazardous_waste_reclassification_description_entry.insert('1.0', data[15])

        self.is_waste_generating_var.set(data[16])
        if data[16] == 1:
            self.wasteGeneratingAdditionalInfo_entry['state'] = 'normal'
            self.wasteGeneratingAdditionalInfo_entry.config(background="white")
            self.wasteGeneratedTerytPk_entry['state'] = 'normal'
            self.wasteGeneratedTerytPk_entry.config(background="white")
            self.wasteGeneratingAdditionalInfo_entry.delete('1.0', tk.END)
            self.wasteGeneratingAdditionalInfo_entry.insert('1.0', data[18])
            self.wasteGeneratedTerytPk_entry.delete('1.0', tk.END)
            self.wasteGeneratedTerytPk_entry.insert('1.0', data[17])

        self.toggle_waste_code_extended()
        self.toggle_hazardous_waste_reclassification()
        self.toggle_waste_generator_extended()

        self.carrier_company_id = data[2]
        self.receiver_company_id = data[3]
        self.EUP_ID = data[4]
        self.own_code = data[5]
        self.process_id = data[9]


    def window(self):
        self.toplevel = tk.Tk()
        self.toplevel.state("zoomed")
        self.wynik = tk.StringVar()
        self.wynik2 = tk.StringVar()
        self.wynik3 = tk.StringVar()


        self.frame00 = tk.Frame(self.toplevel, highlightcolor=self.highlightcolor, highlightthickness=self.highlightthickness,
                                highlightbackground=self.highlightbackground)
        self.frame00.pack(pady=(15, 0), expand=False)
        self.company_info()


        frame1 = tk.Frame(self.toplevel, padx=30)
        frame1.pack(expand=False)

        frame1.grid_columnconfigure(0, weight=1)
        frame1.grid_columnconfigure(1, weight=1)
        frame1.grid_columnconfigure(2, weight=1)


        frame0 = tk.Frame(frame1, highlightcolor=self.highlightcolor, highlightthickness=self.highlightthickness, highlightbackground=self.highlightbackground)
        frame0.grid(pady=10, row=0, column=0, padx=15, sticky=self.sticky_n)

        self.place = self.my_company.show_access_attempt_with_auth(self.company_index)['items'][0]['name']
        self.default_place.GetToken(1).read_access_token_from_csv()

        my_place_label = ttk.Label(frame0, text="Miejsce prowadzenia działalności")
        my_place_label.grid(row=0, column=0, columnspan=2)

        self.my_place_entry = ttk.Entry(frame0, width=40)
        self.my_place_entry.grid(row=1, column=0, pady=(0, 5))
        self.my_place_entry.insert(0, self.place)

        button_my_place = ttk.Button(frame0, width=24, text="Wybierz miejsce",
                                     command=self.open_place_window)
        button_my_place.grid(row=1, column=1, pady=(0, 5))


        frame2 = tk.Frame(frame1, highlightcolor=self.highlightcolor, highlightthickness=self.highlightthickness, highlightbackground=self.highlightbackground)
        frame2.grid(row=1, column=0, pady=(0,5), sticky=self.sticky_n)

        carrier_company_label = ttk.Label(frame2, text="Przewoźnik: *")
        carrier_company_label.grid(row=0, column=0, columnspan=2)

        self.carrier_company_entry = ttk.Entry(frame2, width=40)
        self.carrier_company_entry.grid(row=1, column=0,pady=(0,5))
        self.carrier_company_entry.bind("<Button-1>", lambda event: self.open_transporter_window("przewoznik"))

        self.button = ttk.Button(frame2, width=24, text="Wybierz przewoźnika", command=lambda: self.open_transporter_window("przewoznik"))
        self.button.grid(row=1, column=1,pady=(0,5))


        frame3 = tk.Frame(frame1, highlightcolor=self.highlightcolor, highlightthickness=self.highlightthickness, highlightbackground=self.highlightbackground)
        frame3.grid(pady=10,row=2, column=0, rowspan=1, sticky=self.sticky_n)

        receiver_eup_id_label = ttk.Label(frame3, text="Odbiorca: *")
        receiver_eup_id_label.grid(row=2, column=0, columnspan=2, pady=5)

        self.receiver_eup_id_entry = ttk.Entry(frame3, width=40)
        self.receiver_eup_id_entry.grid(row=3, column=0,pady=(0,8))
        self.receiver_eup_id_entry.bind("<Button-1>", lambda event: self.open_receiver_eup_window())

        self.button1 = ttk.Button(frame3, width=24, text="Wybierz odbiorcę", command=self.open_receiver_eup_window)
        self.button1.grid(row=3,column=1,pady=(0,8))


        frame4 = tk.Frame(frame1, highlightcolor=self.highlightcolor, highlightthickness=self.highlightthickness, highlightbackground=self.highlightbackground)
        frame4.grid(row=3, column=0, sticky=self.sticky_n)

        waste_code_id_label = ttk.Label(frame4, text="Kod Odpadu: *")
        waste_code_id_label.grid(row=0, column=0, columnspan=2, pady=5)

        self.waste_code_id_entry = ttk.Entry(frame4, width=40)
        self.waste_code_id_entry.grid(row=1, column=0,pady=(0,8))
        self.waste_code_id_entry.bind("<Button-1>", lambda event: self.open_waste_window(self.receive_waste_code))

        button4 = ttk.Button(frame4, width=24, text="Wybierz kod odpadu", command=lambda: self.open_waste_window(self.receive_waste_code))
        button4.grid(row=1, column=1,pady=(0,8))


        frame855 = tk.Frame(frame1)
        frame855.grid(pady=10, row=5, column=0, sticky=self.sticky_n)


        frame8 = tk.Frame(frame855, highlightcolor=self.highlightcolor, highlightthickness=self.highlightthickness, highlightbackground=self.highlightbackground)
        frame8.grid(row=0, column=0, sticky=self.sticky_n)

        waste_process_id_label = ttk.Label(frame8, text="Proces Odpadu:")
        waste_process_id_label.grid(row=0, column=0, columnspan=2, pady=3)

        self.waste_process_id_entry = ttk.Entry(frame8, width=40)
        self.waste_process_id_entry.grid(row=1, column=0,pady=(0,8))
        self.waste_process_id_entry.bind("<Button-1>", lambda event: self.open_waste_prcoess_window(self.receive_waste_process))

        button5 = ttk.Button(frame8, width=24, text="Wybierz proces odpadu", command=lambda: self.open_waste_prcoess_window(self.receive_waste_process))
        button5.grid(row=1, column=1,pady=(0,8))


        frame56 = tk.Frame(frame855)
        frame56.grid(pady=(18,0),row=2, column=0, sticky=self.sticky_n)


        frame5 = tk.Frame(frame56, highlightcolor=self.highlightcolor, highlightthickness=self.highlightthickness, highlightbackground=self.highlightbackground)
        frame5.grid(row=0, column=0,padx=(0,14), sticky=self.sticky_n,pady=(0,5))

        vehicle_reg_number_label = ttk.Label(frame5, text="Numer Rejestracyjny Pojazdu: *")
        vehicle_reg_number_label.grid(row=0, column=0, pady=3)

        self.vehicle_reg_number_entry = ttk.Entry(frame5, width=30)
        self.vehicle_reg_number_entry.grid(row=1, column=0,pady=(0,8))


        frame6 = tk.Frame(frame56, highlightcolor=self.highlightcolor, highlightthickness=self.highlightthickness, highlightbackground=self.highlightbackground)
        frame6.grid(row=0, column=1,padx=(14,0), sticky=self.sticky_n)

        vcmd = (self.toplevel.register(self.is_valid_double), '%P')
        inv_cmd = self.toplevel.register(self.on_invalid)

        waste_mass_label = ttk.Label(frame6, text="Masa Odpadu: *")
        waste_mass_label.grid(row=0, column=0, columnspan=8, pady=3)

        self.waste_mass_entry = ttk.Entry(frame6, width=30, validate='key', validatecommand=vcmd, invalidcommand=inv_cmd)
        self.waste_mass_entry.insert(0, "0.0000")
        self.waste_mass_entry.bind('<FocusOut>', self.format_entry)
        self.waste_mass_entry.grid(row=1, column=0, columnspan=6,pady=(0,8))

        waste_mass_label = ttk.Label(frame6, text="w tonach [Mg]")
        waste_mass_label.grid(row=1, column=5, columnspan=2,pady=(0,8))


        frame_list = tk.Frame(frame1, highlightcolor=self.highlightcolor, highlightthickness=self.highlightthickness, highlightbackground=self.highlightbackground)
        frame_list.grid(row=6, column=0)

        self.transmitting_cards_button2 = ttk.Button(frame_list,
                                                    text="Wyświetl karty w których jesteś w roli przekazującego",
                                                    width=60, command=self.open_intermediate_window)
        self.transmitting_cards_button2.grid(row=0, column=0, pady=10, ipady=2)

        self.warming = self.resize_and_display_image('Icons/warning_icon.png',(20,20))
        self.warming_icon = ttk.Button(frame_list, image=self.warming)
        self.warming_icon.grid(row=0, column=1)

        tooltip2 = BothStructure.Tooltip(self.warming_icon, "Pamiętaj aby wybrać miejsce prowadzania działalności")

        self.transmitting_cards_button3 = ttk.Button(frame_list,
                                                     text="Wyświetl karty w których jesteś w roli transportującego",
                                                     width=60, command=self.open_as_transporter)
        self.transmitting_cards_button3.grid(row=1, column=0, pady=10, ipady=2)

        self.warming_icon2 = ttk.Button(frame_list, image=self.warming)
        self.warming_icon2.grid(row=1, column=1)

        tooltip2 = BothStructure.Tooltip(self.warming_icon, "Pamiętaj aby wybrać miejsce prowadzania działalności")

        self.warming_icon.bind("<Enter>", lambda event: tooltip2.show_tooltip())
        self.warming_icon.bind("<Leave>", lambda event: tooltip2.hide_tooltip(event))

        self.warming_icon2.bind("<Enter>", lambda event: tooltip2.show_tooltip())
        self.warming_icon2.bind("<Leave>", lambda event: tooltip2.hide_tooltip(event))


        self.frame7 = tk.Frame(frame1, highlightcolor=self.highlightcolor, highlightthickness=self.highlightthickness, highlightbackground=self.highlightbackground)
        self.frame7.grid(row=0, column=1, pady=10, sticky=self.sticky_n)

        planned_transport_time_label = ttk.Label(self.frame7, text="Planowany Czas Transportu: *")
        planned_transport_time_label.grid(row=0, column=0, columnspan=2)

        self.planned_transport_time_entry = ttk.Entry(self.frame7, width=20)
        self.planned_transport_time_entry.grid(row=1, column=0, padx=(45,0))

        self.calendar_icon = self.resize_and_display_image("Icons/calendar.png", (20, 20))
        self.calendar_button = ttk.Button(self.frame7, width=24, image=self.calendar_icon, command=self.open_calendar)
        self.calendar_button.grid(row=1, column=1,padx=(0,45))


        frame9 = tk.Frame(frame1, highlightcolor=self.highlightcolor, highlightthickness=self.highlightthickness, highlightbackground=self.highlightbackground)
        frame9.grid(row=1, column=1, sticky=self.sticky_n)

        certificate_number_and_box_numbers_label = ttk.Label(frame9, text="Numer Certyfikatu i Numery Paczek:")
        certificate_number_and_box_numbers_label.grid(pady=2)

        self.certificate_number_and_box_numbers_entry = ttk.Entry(frame9, width=40)
        self.certificate_number_and_box_numbers_entry.grid(pady=(0,6))


        frame10 = tk.Frame(frame1, highlightcolor=self.highlightcolor, highlightthickness=self.highlightthickness, highlightbackground=self.highlightbackground)
        frame10.grid(row=2, column=1, pady=10, rowspan=3, sticky=self.sticky_n)

        additional_info_label = ttk.Label(frame10, text="Dodatkowe Informacje:")
        additional_info_label.grid()

        self.additional_info_entry = tk.Text(frame10,foreground="black",borderwidth=0, width=35 , height=8, wrap='word', font=("Arial",9))
        self.additional_info_entry.grid()


        frame11 = tk.Frame(frame1, highlightcolor=self.highlightcolor, highlightthickness=self.highlightthickness, highlightbackground=self.highlightbackground)
        frame11.grid(row=5, column=1, pady=10, rowspan=2, sticky=self.sticky_n)

        waste_code_extended_label = ttk.Label(frame11, text="Rozszerzony Kod Odpadu:")
        waste_code_extended_label.grid(row=0, column=0)

        self.waste_code_extended_var = tk.BooleanVar(value=False)

        waste_code_extended_checkbox = ttk.Checkbutton(frame11, variable=self.waste_code_extended_var,
                                                       command=self.toggle_waste_code_extended)
        waste_code_extended_checkbox.grid(row=0, column=1)

        self.waste_code_extended_description_label = ttk.Label(frame11, text=" ")
        self.waste_code_extended_description_label.grid(row=1, column=0,columnspan=2)

        self.waste_code_extended_description_entry = tk.Text(frame11,foreground="black", width=35 , height=6, wrap='word', font=("Arial",9), state="disabled", background="#f0f0f0", borderwidth=0)
        self.waste_code_extended_description_entry.grid(row=2, column=0, columnspan=2)


        frame110 = tk.Frame(frame1, highlightcolor=self.highlightcolor, highlightthickness=self.highlightthickness, highlightbackground=self.highlightbackground)
        frame110.grid(row=6, column=1, rowspan=2, sticky='w', columnspan=2)

        my_planned_label = tk.Label(frame110, text="Numer karty: ")
        my_planned_label.grid(row=1, column=0, columnspan=2)

        self.my_planned_id_entry = ttk.Entry(frame110, width=35)
        self.my_planned_id_entry.grid(row=2, column=0, columnspan=2)
        self.my_planned_id_entry.insert(0, self.planned_card_id)
        self.my_planned_id_entry.configure(state="disabled", justify='center')

        self.warming_icon4 = ttk.Button(frame110, image=self.warming)
        self.warming_icon4.grid(row=1, column=1)

        tooltip4 = BothStructure.Tooltip(self.warming_icon4, "Wyświetla się przy edycji zatwierdzonej karty")

        self.warming_icon4.bind("<Enter>", lambda event: tooltip4.show_tooltip())
        self.warming_icon4.bind("<Leave>", lambda event: tooltip4.hide_tooltip(event))

        self.transmitting_cards_button3 = ttk.Button(frame110,
                                                     text="Wyświetl karty w których jesteś w roli przejmującego",
                                                     width=60, command=self.open_receiver_card_list)
        self.transmitting_cards_button3.grid(row=0, column=0, pady=10, ipady=2)

        self.warming_icon3 = ttk.Button(frame110, image=self.warming)
        self.warming_icon3.grid(row=0, column=1)

        tooltip3 = BothStructure.Tooltip(self.warming_icon3, "Pamiętaj aby wybrać miejsce prowadzania działalności")

        self.warming_icon3.bind("<Enter>", lambda event: tooltip3.show_tooltip())
        self.warming_icon3.bind("<Leave>", lambda event: tooltip3.hide_tooltip(event))


        frame12 = tk.Frame(frame1, highlightcolor=self.highlightcolor, highlightthickness=self.highlightthickness, highlightbackground=self.highlightbackground)
        frame12.grid(row=0, column=2, pady=10, padx=15, rowspan=2, sticky=self.sticky_n)

        hazardous_waste_reclassification_label = ttk.Label(frame12, text="Reklasyfikacja Odpadów Niebezpiecznych:")
        hazardous_waste_reclassification_label.grid(row=0, column=0, columnspan=3)

        self.hazardous_waste_reclassification_var = tk.BooleanVar(value=False)
        hazardous_waste_reclassification_checkbox = ttk.Checkbutton(frame12,
                                                                    variable=self.hazardous_waste_reclassification_var,
                                                                    command=self.toggle_hazardous_waste_reclassification)
        hazardous_waste_reclassification_checkbox.grid(row=0, column=3)

        self.hazardous_waste_reclassification_description_label = ttk.Label(frame12,
                                                                      text=" ")
        self.hazardous_waste_reclassification_description_label.grid(row=1, column=0, columnspan=4)
        self.hazardous_waste_reclassification_description_entry = tk.Text(frame12,foreground="black", width=35 , height=5, wrap='word', font=("Arial",9), state="disabled", background="#f0f0f0", borderwidth=0)
        self.hazardous_waste_reclassification_description_entry.grid(row=2, column=0, columnspan=4)


        self.frame13 = tk.Frame(frame1, highlightcolor=self.highlightcolor, highlightthickness=self.highlightthickness, highlightbackground=self.highlightbackground)
        self.frame13.grid(row=2, column=2, sticky=self.sticky_n, rowspan=3, pady=10)

        is_waste_generating_label = ttk.Label(self.frame13, text="Generuje Odpady:")
        is_waste_generating_label.grid(row=0, column=0, columnspan=3, pady=5)

        self.is_waste_generating_var = tk.BooleanVar(value=False)

        is_waste_generating_checkbox = ttk.Checkbutton(self.frame13, variable=self.is_waste_generating_var,command=self.toggle_waste_generator_extended)
        is_waste_generating_checkbox.grid(row=0, column=3)

        self.testlabel = ttk.Label(self.frame13, text=" ")
        self.testlabel.grid(row=1, column=0, columnspan=4,pady=3)

        self.wasteGeneratedTerytPk_entry = tk.Text(self.frame13,foreground="black", width=35 , height=1, wrap='word', font=("Arial",9), state="disabled", background="#f0f0f0", borderwidth=0)
        self.wasteGeneratedTerytPk_entry.grid(row=2, column=0, columnspan=4)

        self.waste_additionalInfo = ttk.Label(self.frame13, text=" ")
        self.waste_additionalInfo.grid(row=3, column=0, columnspan=4,pady=2)

        self.wasteGeneratingAdditionalInfo_entry = tk.Text(self.frame13,foreground="black", width=35 , height=3, wrap='word', font=("Arial",9), state="disabled", background="#f0f0f0", borderwidth=0)
        self.wasteGeneratingAdditionalInfo_entry.grid(row=4, column=0, columnspan=4)


        frame14 = tk.Frame(frame1)
        frame14.grid(row=5, column=2, sticky=self.sticky_n,pady=(10,0))

        self.show_details_button = ttk.Button(frame14, text="Historia", command=self.history, width=self.short_button_size)
        self.show_details_button.grid(row=0, column=0, pady=(1,1))

        self.show_details_button = ttk.Button(frame14, text="Wyświetl szczegóły", command=self.details, width=self.short_button_size)
        self.show_details_button.grid(row=1, column=0, pady=(1,1))

        self.save_button = ttk.Button(frame14, text="Stwórz kartę", command=self.save_data, state='disabled', width=self.long_button_size)
        self.save_button.grid(row=4, column=0, columnspan=2, pady=(1,1))

        self.first_waste_button = ttk.Button(frame14, text="Odpad 19 08 01", command=self.first_waste, width=self.short_button_size)
        self.first_waste_button.grid(row=0, column=1, pady=(1,1))

        self.second_waste_button = ttk.Button(frame14, text="Odpad 19 08 02", command=self.second_waste, width=self.short_button_size)
        self.second_waste_button.grid(row=1, column=1, pady=(1,1))

        self.third_waste_button = ttk.Button(frame14, text="Odpad 19 08 14", command=self.third_waste, width=self.short_button_size)
        self.third_waste_button.grid(row=2, column=1, pady=(1,1))

        self.edit_button= ttk.Button(frame14, text="Edytuj istniejącą kartę", command=self.edit_card, width=self.long_button_size)
        self.edit_button.grid(row=3, column=0, columnspan=2, pady=(1,1))
        self.edit_button.configure(state="disabled")

        self.reset_all = ttk.Button(frame14, text="Resetuj", command=self.reset, width=self.short_button_size)
        self.reset_all.grid(row=2, column=0, pady=(1,0))

        for entry in [self.carrier_company_entry, self.receiver_eup_id_entry,self.waste_code_id_entry, self.vehicle_reg_number_entry, self.waste_mass_entry,
                self.planned_transport_time_entry]:
            entry.bind("<KeyRelease>", self.check_fields)

        self.toplevel.mainloop()



    def open_receiver_card_list(self):
        try:

            if self.child_window_receiver and self.child_window_receiver.winfo_exists():
                self.child_window_receiver.deiconify()
            else:
                raise AttributeError
        except AttributeError:

            self.child_window_receiver = AllCardsAsReceiver.CardsListApplication(self.company_index,
                                                                                 callback=self.on_window_receiver_opened)

            self.child_window_receiver.create_widgets()


    def on_window_receiver_opened(self, child_window):
        self.child_window_receiver = child_window



    def open_as_transporter(self):
        try:
            if self.child_window_transporter and self.child_window_transporter.winfo_exists():
                self.child_window_transporter.deiconify()
            else:
                raise AttributeError
        except AttributeError:
            self.child_window_transporter = AllCardsAsTransporter.CardsListApplication(self.company_index,
                                                                                       callback=self.on_window_opened)
            self.child_window_transporter.create_widgets()



    def open_intermediate_window(self):
        try:
            if self.child_window_transmitter and self.child_window_transmitter.winfo_exists():
                self.child_window_transmitter.deiconify()
            else:
                raise AttributeError
        except AttributeError:
            self.place_index = self.company_index
            self.child_window_transmitter = MainTransmitterWindow.CardStatusWindow(None, self.place_index,
                                                                         self.on_intermediate_window_selection,
                                                                         self.toplevel)
            self.child_window_transmitter.test()


    def on_intermediate_window_selection(self, selection, window):
        self.child_window_transmitter = window
        if selection == 'Planowana':
            self.open_planned_card_list(window)
        elif selection == 'Wycofana':
            self.open_withdrawn_card_list()
        elif selection == "Potwierdzenie wygenerowane":
            self.open_confirmation_generated_card_list()
        elif selection == "Wszystkie":
            self.open_all_list()
        elif selection =="Potwierdzona":
            self.open_approved_card_list(window)
        elif selection =="Potwierdzenie przejęcia":
            self.open_receive_confirmation_card_list()
        elif selection =="Odrzucona":
            self.open_rejected_card_list()
        elif selection =="Potwierdzony transport":
            self.open_transport_confirmation_card_list()
        else:
            print(f"Nieznany wybór: {selection}")


    def open_planned_card_list(self, window):
        PlannedCardList.CardsListApplication(window, callback=self.edit_callback).create_widgets()


    def open_approved_card_list(self, window):
        ApprovedCardList.CardsListApplication(window, callback=self.edit_callback_confirmed).create_widgets()


    @staticmethod
    def open_confirmation_generated_card_list():
        ConfirmationGeneratedCardList.CardsListApplication().create_widgets()


    @staticmethod
    def open_receive_confirmation_card_list():
        ReceiveConfirmationCardList.CardsListApplication().create_widgets()


    @staticmethod
    def open_transport_confirmation_card_list():
        TransportConfirmationCardList.CardsListApplication().create_widgets()


    @staticmethod
    def open_all_list():
        AllCardsAsTransmitter.CardsListApplication().create_widgets()


    def on_window_opened(self, child_window):
        self.child_window_transporter = child_window


    @staticmethod
    def open_withdrawn_card_list():
        WithdrawnCardList.CardsListApplication().create_widgets()


    @staticmethod
    def open_rejected_card_list():
        RejectedCardList.CardsListApplication().create_widgets()


    def reset(self):
        self.button.configure(state="normal")
        self.carrier_company_entry.configure(state="normal")
        self.button1.configure(state="normal")
        self.receiver_eup_id_entry.configure(state="normal")

        self.carrier_company_entry.delete(0, tk.END)
        self.receiver_eup_id_entry.delete(0, tk.END)
        self.waste_code_id_entry.delete(0, tk.END)
        self.waste_process_id_entry.delete(0, tk.END)
        self.vehicle_reg_number_entry.delete(0, tk.END)
        self.waste_mass_entry.delete(0, tk.END)
        self.waste_mass_entry.insert(0,"0.0000")
        self.planned_transport_time_entry.delete(0, tk.END)
        self.certificate_number_and_box_numbers_entry.delete(0, tk.END)
        self.additional_info_entry.delete("1.0", tk.END)
        self.waste_code_extended_description_entry.delete("1.0", tk.END)
        self.hazardous_waste_reclassification_description_entry.delete("1.0", tk.END)
        self.wasteGeneratedTerytPk_entry.delete("1.0", tk.END)
        self.wasteGeneratingAdditionalInfo_entry.delete("1.0", tk.END)
        self.my_planned_id_entry.configure(state="normal")
        self.my_planned_id_entry.delete(0, tk.END)
        self.my_planned_id_entry.insert(0, "brak, wybierz kartę")
        self.my_planned_id_entry.configure(state="disabled")
        self.edit_button.configure(state="disabled")

        self.DateCorrect = False

        self.carrier_company_id = None
        self.receiver_company_id = None
        self.EUP_ID = None
        self.own_code = None
        self.VehicleRegNumber = None
        self.WasteMass = None
        self.PlannedTransportTime = None
        self.process_id = None
        self.CertificateNumberAndBoxNumbers = None
        self.AdditionaInfo = None
        self.waste_code_extended = None
        self.WasteCodeExtendedDescription = None
        self.hazardous_waste_reclassification = None
        self.HazardousWasteReclassificationDescription = None
        self.is_waste_generating = None
        self.WasteGeneratedTerytPk = None
        self.WasteGeneratingAdditionalInfo = None

        self.waste_code_extended_var.set(False)
        self.hazardous_waste_reclassification_var.set(False)
        self.is_waste_generating_var.set(False)

        if self.search_teryt_button_created:
            self.search_teryt_button.destroy()
            self.search_teryt_button_created = False

        self.save_button['state'] = 'disabled'
        self.edit_button['state'] = 'disabled'

        self.toggle_hazardous_waste_reclassification()
        self.toggle_waste_code_extended()
        self.toggle_waste_generator_extended()
        self.EditState = None


    def company_info(self):
        self.company = CompanyLabel.CompanyFrame(self.frame00, 0, 0, self.toplevel, 104)
        self.company.main_frame()


    def edit_callback_confirmed(self, data):
        print("Otrzymano dane z okna Toplevel:", data)
        table = data[0]
        self.card_id_edit = table[0]
        self.planned_transport_time_edit = table[1]
        self.real_time_edit = table[2]
        self.waste_code_edit = table[3]
        self.waste_code_descpription_edit = table[4]
        self.vehicle_reg_edit = table[5]
        self.card_type_edit = table[6]
        self.sender_company_name_edit = table[7]
        self.carrier_name_edit = table[8]
        table2 = data[1]
        self.year_edit = table2['year']
        self.sender_company_id_edit = table2['senderCompanyId']
        self.sender_company_eup_edit = table2['senderEupId']
        self.carrier_company_id_edit = table2['carrierCompanyId']
        self.receiver_company_id_edit = table2['receiverCompanyId']
        self.receiver_eup_id_edit = table2['receiverEupId']
        self.waste_code_id_edit = table2['wasteCodeId']
        self.waste_mass_edit = table2['wasteMass']
        self.waste_process_id_edit = table2['wasteProcessId']
        self.certificate_number_and_box_numbers_edit = table2['certificateNumberAndBoxNumbers']
        self.card_status_code_name_edit = table2['cardStatusCodeName']
        self.additional_info_edit = table2['additionalInfo']
        self.waste_code_extended_edit = table2['wasteCodeExtended']
        self.waste_code_extended_description_edit = table2['wasteCodeExtendedDescription']
        self.hazardous_waste_reclassification_edit = table2['hazardousWasteReclassification']
        self.hazardous_waste_reclassification_description_edit = table2['hazardousWasteReclassificationDescription']
        self.is_waste_generating_edit = table2['isWasteGenerating']
        self.waste_generated_teryt_edit = table2['wasteGeneratedTeryt']
        self.waste_generating_additional_info_edit = table2['wasteGeneratingAdditionalInfo']
        self.waste_generated_teryt_pk_edit = table2['wasteGeneratedTerytPk']
        self.edit_button.configure(state='normal')
        self.save_button.configure(state='disabled')

        list = KpoRequests.Search().WyszukiwarkaPoCopmanyID(self.receiver_company_id_edit)
        name = list['name']

        self.carrier_company_entry.delete(0, tk.END)
        self.carrier_company_entry.insert(0, self.carrier_name_edit)
        self.receiver_eup_id_entry.delete(0, tk.END)
        self.receiver_eup_id_entry.insert(0, name)

        self.waste_code_id_entry.delete(0, tk.END)
        self.waste_code_id_entry.insert(0, self.waste_code_edit)

        self.waste_process_id_entry.delete(0, tk.END)
        if self.waste_process_id_edit is not None:
            self.waste_process_id_entry.insert(0, str(self.waste_process_id_edit))
        else:
            print("Wartość waste_process_id_edit jest None lub nieprawidłowa")

        self.vehicle_reg_number_entry.delete(0, tk.END)
        self.vehicle_reg_number_entry.insert(0, self.vehicle_reg_edit)
        self.waste_mass_entry.delete(0, tk.END)
        self.waste_mass_entry.insert(0, self.waste_mass_edit)
        self.planned_transport_time_entry.delete(0, tk.END)
        self.planned_time = self.remove_t_from_date(self.planned_transport_time_edit)
        self.planned_transport_time_entry.insert(0, self.planned_time)
        self.certificate_number_and_box_numbers_entry.delete(0, tk.END)
        self.certificate_number_and_box_numbers_entry.insert(0, self.certificate_number_and_box_numbers_edit)
        self.additional_info_entry.delete('1.0', tk.END)
        self.additional_info_entry.insert('1.0', self.additional_info_edit)
        self.waste_code_extended_var.set(self.waste_code_extended_edit)

        if self.waste_code_extended_edit == 1:
            self.waste_code_extended_description_entry['state'] = 'normal'
            self.waste_code_extended_description_entry.config(background="white")
            self.waste_code_extended_description_entry.delete('1.0', tk.END)
            self.waste_code_extended_description_entry.insert('1.0', self.waste_code_extended_description_edit)

        self.hazardous_waste_reclassification_var.set(self.hazardous_waste_reclassification_edit)
        if self.hazardous_waste_reclassification_edit == 1:
            self.hazardous_waste_reclassification_description_entry['state'] = 'normal'
            self.hazardous_waste_reclassification_description_entry.config(background="white")
            self.hazardous_waste_reclassification_description_entry.delete('1.0', tk.END)
            self.hazardous_waste_reclassification_description_entry.insert('1.0',
                                                                           self.hazardous_waste_reclassification_description_edit)

        if self.waste_generated_teryt_edit == 1:
            self.wasteGeneratingAdditionalInfo_entry['state'] = 'normal'
            self.wasteGeneratingAdditionalInfo_entry.config(background="white")
            self.wasteGeneratedTerytPk_entry['state'] = 'normal'
            self.wasteGeneratedTerytPk_entry.config(background="white")
            self.wasteGeneratingAdditionalInfo_entry.delete('1.0', tk.END)
            self.wasteGeneratingAdditionalInfo_entry.insert('1.0', self.waste_generating_additional_info_edit)
            self.wasteGeneratedTerytPk_entry.delete('1.0', tk.END)
            self.wasteGeneratedTerytPk_entry.insert('1.0', self.waste_generated_teryt_pk_edit)

        self.carrier_company_id = self.carrier_company_id_edit
        self.receiver_company_id = self.receiver_company_id_edit
        self.EUP_ID = self.receiver_eup_id_edit
        self.own_code = self.waste_code_id_edit
        self.VehicleRegNumber = self.vehicle_reg_edit
        self.WasteMass = self.waste_mass_edit
        self.PlannedTransportTime = self.planned_transport_time_edit
        self.process_id = self.waste_process_id_edit
        self.CertificateNumberAndBoxNumbers = self.certificate_number_and_box_numbers_edit
        self.AdditionaInfo = self.additional_info_edit
        self.waste_code_extended = self.waste_code_extended_edit
        self.WasteCodeExtendedDescription = self.waste_code_extended_description_edit
        self.hazardous_waste_reclassification = self.hazardous_waste_reclassification_edit
        self.HazardousWasteReclassificationDescription = self.hazardous_waste_reclassification_description_edit
        self.is_waste_generating = self.is_waste_generating_edit
        self.WasteGeneratedTerytPk = self.waste_generated_teryt_pk_edit
        self.WasteGeneratingAdditionalInfo = self.waste_generating_additional_info_edit

        card_number = table2['cardNumber']

        self.my_planned_id_entry.configure(state="normal")
        self.my_planned_id_entry.delete(0, tk.END)

        if card_number == "None" or card_number == None:
            self.my_planned_id_entry.insert(0, "Ta karta nie posiada jeszcze numeru")
        else:
            self.my_planned_id_entry.insert(0, card_number)

        self.my_planned_id_entry.configure(state="disabled")

        self.carrier_company_entry.configure(state="disabled")
        self.button.configure(state="disabled")
        self.button1.configure(state="disabled")
        self.receiver_eup_id_entry.configure(state="disabled")
        self.EditState = 1


    def edit_callback(self, data):
        print("Otrzymano dane z okna Toplevel:", data)
        table = data[0]
        self.card_id_edit = table[0]
        self.planned_transport_time_edit = table[1]
        self.real_time_edit = table[2]
        self.waste_code_edit = table[3]
        self.waste_code_descpription_edit = table[4]
        self.vehicle_reg_edit = table[5]
        self.card_type_edit = table[6]
        self.sender_company_name_edit = table[7]
        self.carrier_name_edit = table[8]
        table2 = data[1]
        self.year_edit = table2['year']
        self.sender_company_id_edit = table2['senderCompanyId']
        self.sender_company_eup_edit = table2['senderEupId']
        self.carrier_company_id_edit = table2['carrierCompanyId']
        self.receiver_company_id_edit = table2['receiverCompanyId']
        self.receiver_eup_id_edit = table2['receiverEupId']
        self.waste_code_id_edit = table2['wasteCodeId']
        self.waste_mass_edit = table2['wasteMass']
        self.waste_process_id_edit = table2['wasteProcessId']
        self.certificate_number_and_box_numbers_edit = table2['certificateNumberAndBoxNumbers']
        self.card_status_code_name_edit = table2['cardStatusCodeName']
        self.additional_info_edit = table2['additionalInfo']
        self.waste_code_extended_edit = table2['wasteCodeExtended']
        self.waste_code_extended_description_edit = table2['wasteCodeExtendedDescription']
        self.hazardous_waste_reclassification_edit = table2['hazardousWasteReclassification']
        self.hazardous_waste_reclassification_description_edit = table2['hazardousWasteReclassificationDescription']
        self.is_waste_generating_edit = table2['isWasteGenerating']
        self.waste_generated_teryt_edit = table2['wasteGeneratedTeryt']
        self.waste_generating_additional_info_edit = table2['wasteGeneratingAdditionalInfo']
        self.waste_generated_teryt_pk_edit = table2['wasteGeneratedTerytPk']
        self.edit_button.configure(state='normal')
        self.save_button.configure(state='disabled')

        list = KpoRequests.Search().WyszukiwarkaPoCopmanyID(self.receiver_company_id_edit)
        name = list['name']

        self.carrier_company_entry.delete(0, tk.END)
        self.carrier_company_entry.insert(0, self.carrier_name_edit)
        self.receiver_eup_id_entry.delete(0, tk.END)
        self.receiver_eup_id_entry.insert(0, name)

        self.waste_code_id_entry.delete(0, tk.END)
        self.waste_code_id_entry.insert(0, self.waste_code_edit)

        self.waste_process_id_entry.delete(0, tk.END)
        if self.waste_process_id_edit is not None:
            self.waste_process_id_entry.insert(0, str(self.waste_process_id_edit))
        else:
            print("Wartość waste_process_id_edit jest None lub nieprawidłowa")

        self.vehicle_reg_number_entry.delete(0, tk.END)
        self.vehicle_reg_number_entry.insert(0, self.vehicle_reg_edit)
        self.waste_mass_entry.delete(0, tk.END)
        self.waste_mass_entry.insert(0, self.waste_mass_edit)
        self.planned_transport_time_entry.delete(0, tk.END)
        self.planned_time = self.remove_t_from_date(self.planned_transport_time_edit)
        self.planned_transport_time_entry.insert(0, self.planned_time)
        self.certificate_number_and_box_numbers_entry.delete(0, tk.END)
        self.certificate_number_and_box_numbers_entry.insert(0, self.certificate_number_and_box_numbers_edit)
        self.additional_info_entry.delete('1.0', tk.END)
        self.additional_info_entry.insert('1.0', self.additional_info_edit)
        self.waste_code_extended_var.set(self.waste_code_extended_edit)

        if self.waste_code_extended_edit == 1:
            self.waste_code_extended_description_entry['state'] = 'normal'
            self.waste_code_extended_description_entry.config(background="white")
            self.waste_code_extended_description_entry.delete('1.0', tk.END)
            self.waste_code_extended_description_entry.insert('1.0', self.waste_code_extended_description_edit)

        self.hazardous_waste_reclassification_var.set(self.hazardous_waste_reclassification_edit)
        if self.hazardous_waste_reclassification_edit == 1:
            self.hazardous_waste_reclassification_description_entry['state'] = 'normal'
            self.hazardous_waste_reclassification_description_entry.config(background="white")
            self.hazardous_waste_reclassification_description_entry.delete('1.0', tk.END)
            self.hazardous_waste_reclassification_description_entry.insert('1.0', self.hazardous_waste_reclassification_description_edit)

        if self.waste_generated_teryt_edit == 1:
            self.wasteGeneratingAdditionalInfo_entry['state'] = 'normal'
            self.wasteGeneratingAdditionalInfo_entry.config(background="white")
            self.wasteGeneratedTerytPk_entry['state'] = 'normal'
            self.wasteGeneratedTerytPk_entry.config(background="white")
            self.wasteGeneratingAdditionalInfo_entry.delete('1.0', tk.END)
            self.wasteGeneratingAdditionalInfo_entry.insert('1.0', self.waste_generating_additional_info_edit)
            self.wasteGeneratedTerytPk_entry.delete('1.0', tk.END)
            self.wasteGeneratedTerytPk_entry.insert('1.0', self.waste_generated_teryt_pk_edit)

        self.carrier_company_id  = self.carrier_company_id_edit
        self.receiver_company_id = self.receiver_company_id_edit
        self.EUP_ID = self.receiver_eup_id_edit
        self.own_code = self.waste_code_id_edit
        self.VehicleRegNumber = self.vehicle_reg_edit
        self.WasteMass = self.waste_mass_edit
        self.PlannedTransportTime = self.planned_transport_time_edit
        self.process_id = self.waste_process_id_edit
        self.CertificateNumberAndBoxNumbers = self.certificate_number_and_box_numbers_edit
        self.AdditionaInfo = self.additional_info_edit
        self.waste_code_extended = self.waste_code_extended_edit
        self.WasteCodeExtendedDescription = self.waste_code_extended_description_edit
        self.hazardous_waste_reclassification = self.hazardous_waste_reclassification_edit
        self.HazardousWasteReclassificationDescription = self.hazardous_waste_reclassification_description_edit
        self.is_waste_generating = self.is_waste_generating_edit
        self.WasteGeneratedTerytPk = self.waste_generated_teryt_pk_edit
        self.WasteGeneratingAdditionalInfo = self.waste_generating_additional_info_edit

        card_number = table2['cardNumber']

        self.my_planned_id_entry.configure(state="normal")
        self.my_planned_id_entry.delete(0, tk.END)

        if card_number == "None" or card_number == None:
            self.my_planned_id_entry.insert(0, "Ta karta nie posiada jeszcze numeru")
        else:
            self.my_planned_id_entry.insert(0, card_number)

        self.my_planned_id_entry.configure(state="disabled")
        self.EditState = 0


    @staticmethod
    def remove_t_from_date(date_string):
        if 'T' in date_string:

            cleaned_date = date_string.replace('T', ' ')
            return cleaned_date
        else:
            return date_string


    def edit_card(self):
        if self.EditState == 0:
            new_data = self.gather_all_data()
            print("HALO")
            print("TO NOWE DANE "+str(new_data))

            data = {
                "KpoId": self.card_id_edit,
                "CarrierCompanyId": new_data['CarrierCompanyId'],
                "ReceiverCompanyId": new_data['ReceiverCompanyId'],
                "ReceiverEupId": new_data['ReceiverEupId'],
                "WasteCodeId": new_data['WasteCodeId'],
                "VehicleRegNumber": new_data['VehicleRegNumber'],
                "WasteMass": new_data['WasteMass'],
                "PlannedTransportTime": new_data['PlannedTransportTime'],

                "WasteProcessId": new_data['WasteProcessId'],
                "CertificateNumberAndBoxNumbers": new_data['CertificateNumberAndBoxNumbers'],
                "AdditionalInfo": new_data['AdditionalInfo'],
                "WasteCodeExtended": new_data['WasteCodeExtended'],
                "WasteCodeExtendedDescription": new_data['WasteCodeExtendedDescription'],
                "HazardousWasteReclassification": new_data['HazardousWasteReclassification'],
                "HazardousWasteReclassificationDescription": new_data['HazardousWasteReclassificationDescription'],
                "IsWasteGenerating": new_data['IsWasteGenerating'],
                "WasteGeneratedTerytPk": new_data['WasteGeneratedTerytPk'],
                "WasteGeneratingAdditionalInfo": new_data['WasteGeneratingAdditionalInfo']
            }

            KpoRequests.KPO().edycja_karty_ze_statusem_planowana(data,self.toplevel)

            try:
                if hasattr(self, 'child_window_receiver') and self.child_window_receiver is not None:
                    self.child_window_receiver.destroy()
                    self.child_window_receiver = None
                if hasattr(self, 'child_window_transmitter') and self.child_window_transmitter is not None:
                    self.child_window_transmitter.destroy()
                    self.child_window_transmitter = None
                if hasattr(self, 'child_window_transporter') and self.child_window_transporter is not None:
                    self.child_window_transporter.destroy()
                    self.child_window_transporter = None
            except Exception as e:
                print(f"Wystąpił błąd podczas zamykania okien: {e}")

            self.reset()

        elif self.EditState == 1:
            new_data = self.collect_edit_data()
            print("To nowe dane: "+str(new_data))
            KpoRequests.KPO().edycja_karty_ze_statusem_zatwierdzona(new_data, self.toplevel)
            self.reset()

        else:
            print("błąd")


    @staticmethod
    def replace_comma_with_dot(input_string):
        return input_string.replace(',', '.')


    def first_waste(self):
        self.clear_fields()
        self.my_place_entry.insert(0,self.place)
        self.carrier_company_entry.insert(0, self.my_carrier_company_name)
        self.carrier_company_id = self.my_carrier_company_id
        self.receiver_eup_id_entry.insert(0, self.my_receiver_company_name)
        self.receiver_company_id = self.my_receiver_company_id
        self.EUP_ID = self.my_receiver_company_eup
        self.waste_code_id_entry.insert(0, "19 08 01")
        self.own_code = "953"
        self.vehicle_reg_number_entry.insert(0, self.my_reg_vehicle)
        self.waste_mass_entry.insert(0, "0,0000")


    def second_waste(self):
        self.clear_fields()
        self.my_place_entry.insert(0, self.place)
        self.carrier_company_entry.insert(0, self.my_carrier_company_name)
        self.carrier_company_id = self.my_carrier_company_id
        self.receiver_eup_id_entry.insert(0, self.my_receiver_company_name)
        self.receiver_company_id = self.my_receiver_company_id
        self.EUP_ID = self.my_receiver_company_eup
        self.waste_code_id_entry.insert(0, "19 08 02")
        self.own_code = "954"
        self.vehicle_reg_number_entry.insert(0, self.my_reg_vehicle)
        self.waste_mass_entry.insert(0, "0,0000")


    def third_waste(self):
        self.clear_fields()
        self.my_place_entry.insert(0, self.place)
        self.carrier_company_entry.insert(0, self.my_carrier_company_name)
        self.carrier_company_id = self.my_carrier_company_id
        self.receiver_eup_id_entry.insert(0, self.my_receiver_company_name)
        self.receiver_company_id = self.my_receiver_company_id
        self.EUP_ID = self.my_receiver_company_eup
        self.waste_code_id_entry.insert(0, "19 08 14")
        self.own_code = "964"
        self.vehicle_reg_number_entry.insert(0, self.my_reg_vehicle)
        self.waste_mass_entry.insert(0, "0,0000")


    def clear_fields(self):

        self.my_place_entry.delete(0, tk.END)
        self.carrier_company_entry.delete(0, tk.END)
        self.receiver_eup_id_entry.delete(0, tk.END)
        self.waste_code_id_entry.delete(0, tk.END)
        self.waste_process_id_entry.delete(0, tk.END)
        self.vehicle_reg_number_entry.delete(0, tk.END)
        self.waste_mass_entry.delete(0, tk.END)
        self.planned_transport_time_entry.delete(0, tk.END)
        self.certificate_number_and_box_numbers_entry.delete(0, tk.END)
        self.additional_info_entry.delete("1.0", tk.END)
        self.waste_code_extended_description_entry.delete("1.0", tk.END)
        self.hazardous_waste_reclassification_description_entry.delete("1.0", tk.END)
        self.wasteGeneratedTerytPk_entry.delete("1.0", tk.END)
        self.wasteGeneratingAdditionalInfo_entry.delete("1.0", tk.END)
        self.my_planned_id_entry.configure(state="normal")
        self.my_planned_id_entry.delete(0,tk.END)
        self.my_planned_id_entry.insert(0, "brak, wybierz kartę")
        self.my_planned_id_entry.configure(state="disabled")
        self.edit_button.configure(state="disabled")


    def save_data_to_database(self):
        host = self.host
        user = self.user
        password = self.password
        db = self.database

        connection = mysql.connector.connect(host=host, user=user, password=password, database=db)
        cursor = connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dane_karty (
                id INT AUTO_INCREMENT PRIMARY KEY,
                Creator TEXT,
                CarrierCompanyId TEXT,
                ReceiverCompanyId TEXT,
                ReceiverEupId TEXT,
                WasteCodeId TEXT,
                VehicleRegNumber TEXT,
                WasteMass TEXT,
                PlannedTransportTime TEXT,
                WasteProcessId TEXT,
                CertificateNumberAndBoxNumbers TEXT,
                AdditionalInfo TEXT,
                WasteCodeExtended BOOLEAN,
                WasteCodeExtendedDescription TEXT,
                HazardousWasteReclassification BOOLEAN,
                HazardousWasteReclassificationDescription TEXT,
                IsWasteGenerating BOOLEAN,
                WasteGeneratedTerytPk TEXT,
                WasteGeneratingAdditionalInfo TEXT,
                ReceiverCompanyName TEXT,
                TransporterCompanyName TEXT,
                CodeNumber TEXT,
                ProcessName TEXT
            )''')

        sql = """INSERT INTO dane_karty (CarrierCompanyId, Creator,ReceiverCompanyId, ReceiverEupId, WasteCodeId,
                 VehicleRegNumber, WasteMass, PlannedTransportTime, WasteProcessId, CertificateNumberAndBoxNumbers,
                 AdditionalInfo, WasteCodeExtended, WasteCodeExtendedDescription, HazardousWasteReclassification,
                 HazardousWasteReclassificationDescription, IsWasteGenerating, WasteGeneratedTerytPk, WasteGeneratingAdditionalInfo,
                 ReceiverCompanyName,TransporterCompanyName, CodeNumber, ProcessName)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        data = (self.CarrierCompanyId, self.creator, self.ReceiverCompanyId, self.ReceiverEupId, self.WasteCodeId,
                self.VehicleRegNumber, self.WasteMass, self.PlannedTransportTime, self.WasteProcessId,
                self.CertificateNumberAndBoxNumbers, self.AdditionaInfo, self.waste_code_extended,
                self.WasteCodeExtendedDescription, self.hazardous_waste_reclassification,
                self.HazardousWasteReclassificationDescription, self.is_waste_generating,
                self.WasteGeneratedTerytPk, self.WasteGeneratingAdditionalInfo, self.carrier_company_entry.get(), self.receiver_eup_id_entry.get(),
                self.waste_code_id_entry.get(), self.waste_process_id_entry.get())

        try:
            cursor.execute(sql, data)
            connection.commit()
            print("Dane zostały zapisane w bazie danych.")
        except mysql.connector.Error as err:
            print(f"Wystąpił błąd: {err}")
        finally:
            connection.close()


    @staticmethod
    def is_valid_double(user_input):
        if user_input in ["", ".", ",", "0.0000"]:
            return True

        try:
            user_input = user_input.replace(',', '.')
            parts = user_input.split('.')
            if len(parts) > 2:
                return False

            if len(parts) == 2 and len(parts[1]) > 4:
                return False

            float(user_input)
            return True
        except ValueError:
            return False


    @staticmethod
    def on_invalid():
        print("Niewłaściwe dane. Wpisz wartość double z maksymalnie 4 miejscami po przecinku.")


    def format_entry(self, event):
        content = self.waste_mass_entry.get()
        if content and '.' in content:
            parts = content.split('.')
            if len(parts[1]) < 4:
                content = content + '0' * (4 - len(parts[1]))
                self.waste_mass_entry.delete(0, tk.END)
                self.waste_mass_entry.insert(0, content)


    def details(self):
        data = self.gather_all_data()
        DetalisPlanCard.PlannedCardDetails(data).window()


    def check_fields(self, event=None):
        fields_filled = all([
            self.carrier_company_entry.get(),
            self.receiver_eup_id_entry.get(),
            self.waste_code_id_entry.get(),
            self.vehicle_reg_number_entry.get(),
            self.waste_mass_entry.get() != "0.0000",
            self.planned_transport_time_entry.get(),
        ])

        edit_button_disabled = 'disabled' in self.edit_button.state()
        if fields_filled and self.DateCorrect and edit_button_disabled:
            self.save_button['state'] = 'normal'
        else:
            self.save_button['state'] = 'disabled'


    @staticmethod
    def format_date(date_str):
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            return date_obj.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        except ValueError:
            return None


    @staticmethod
    def reverse_format_date(date_str):
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
            return date_obj.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            return None


    def toggle_waste_generator_extended(self):
        if self.is_waste_generating_var.get():

            self.wasteGeneratedTerytPk_entry['state'] = 'normal'
            self.wasteGeneratedTerytPk_entry.config(background="white")
            self.wasteGeneratingAdditionalInfo_entry['state'] = 'normal'
            self.wasteGeneratingAdditionalInfo_entry.config(background="white")
            self.waste_additionalInfo.config(text="Opis Rozszerzonego Kodu Odpadu:")
            self.search_teryt_button = ttk.Button(self.frame13, text="Wyszukaj kod Teryt",
                                                  command=self.open_teryt_window)
            self.search_teryt_button.grid(row=1, column=0, columnspan=4, sticky='ew')
            self.search_teryt_button_created = True

            if hasattr(self, 'testlabel'):
                self.testlabel.destroy()

            if not hasattr(self, 'search_teryt_button'):
                self.search_teryt_button = ttk.Button(self.frame13, text="Wyszukaj kod Teryt",
                                                      command=self.open_teryt_window)
                self.search_teryt_button.grid(row=1, column=0, columnspan=4, sticky='ew')
                self.search_teryt_button_created = True
        else:

            self.wasteGeneratedTerytPk_entry.delete('1.0', tk.END)
            self.wasteGeneratedTerytPk_entry['state'] = 'disabled'
            self.wasteGeneratedTerytPk_entry.config(background="#f0f0f0")
            self.wasteGeneratingAdditionalInfo_entry.delete('1.0', tk.END)
            self.wasteGeneratingAdditionalInfo_entry['state'] = 'disabled'
            self.wasteGeneratingAdditionalInfo_entry.config(background="#f0f0f0")
            self.waste_additionalInfo.config(text=" ")

            if hasattr(self, 'search_teryt_button') and self.search_teryt_button_created:
                self.search_teryt_button.destroy()

            if not hasattr(self, 'testlabel') or not self.testlabel.winfo_exists():
                self.testlabel = ttk.Label(self.frame13, text=" ")
                self.testlabel.grid(row=1, column=0, columnspan=4, pady=3)


    def toggle_waste_code_extended(self):
        if self.waste_code_extended_var.get():
            self.waste_code_extended_description_entry['state'] = 'normal'
            self.waste_code_extended_description_entry.config(background="white")
            self.waste_code_extended_description_label.config(text="Opis Rozszerzonego Kodu Odpadu:")
        else:
            self.waste_code_extended_description_entry.delete('1.0', tk.END)
            self.waste_code_extended_description_entry.config(background="#f0f0f0")
            self.waste_code_extended_description_label.config(text=" ")
            self.waste_code_extended_description_entry['state'] = 'disabled'


    def toggle_hazardous_waste_reclassification(self):
        if self.hazardous_waste_reclassification_var.get():
            self.hazardous_waste_reclassification_description_entry['state'] = 'normal'
            self.hazardous_waste_reclassification_description_entry.config(background="white")
            self.hazardous_waste_reclassification_description_label.config(text="Opis: ")
        else:
            self.hazardous_waste_reclassification_description_entry.delete('1.0', tk.END)
            self.hazardous_waste_reclassification_description_entry['state'] = 'disabled'
            self.hazardous_waste_reclassification_description_entry.config(background="#f0f0f0")
            self.hazardous_waste_reclassification_description_label.config(text=" ")


    def collect_edit_data(self):
        self.ReceiverEupId = self.EUP_ID if hasattr(self, 'EUP_ID') else None
        self.WasteCodeId = self.own_code if hasattr(self, 'own_code') else None
        self.VehicleRegNumber = self.vehicle_reg_number_entry.get() if hasattr(self,
                                                                               'vehicle_reg_number_entry') else None
        self.WasteMass = self.waste_mass_entry.get() if hasattr(self, 'waste_mass_entry') else None
        self.PrePlannedTransportTime = self.planned_transport_time_entry.get() if hasattr(self,
                                                                                          'planned_transport_time_entry') else None
        self.PlannedTransportTime = self.format_date(self.PrePlannedTransportTime) if hasattr(self,
                                                                                              'PrePlannedTransportTime') else None
        self.WasteProcessId = self.process_id if hasattr(self, 'process_id') else None
        self.CertificateNumberAndBoxNumbers = self.certificate_number_and_box_numbers_entry.get() if hasattr(self,
                                                                                                             'certificate_number_and_box_numbers_entry') else None
        self.AdditionaInfo = self.additional_info_entry.get("1.0", "end-1c") if hasattr(self,
                                                                                        'additional_info_entry') else None
        self.waste_code_extended = self.waste_code_extended_var.get() if hasattr(self,
                                                                                 'waste_code_extended_var') else None
        if self.waste_code_extended == True:
            self.WasteCodeExtendedDescription = self.waste_code_extended_description_entry.get("1.0",
                                                                                               "end-1c") if hasattr(
                self, 'waste_code_extended_description_entry') else None
        else:
            self.WasteCodeExtendedDescription = None
        self.hazardous_waste_reclassification = self.hazardous_waste_reclassification_var.get() if hasattr(self,
                                                                                                           'hazardous_waste_reclassification_var') else None
        if self.hazardous_waste_reclassification == True:
            self.HazardousWasteReclassificationDescription = self.hazardous_waste_reclassification_description_entry.get(
                "1.0", "end-1c") if hasattr(self, 'hazardous_waste_reclassification_description_entry') else None
        else:
            self.HazardousWasteReclassificationDescription = None
        self.is_waste_generating = self.is_waste_generating_var.get() if hasattr(self,
                                                                                 'is_waste_generating_var') else None
        if self.is_waste_generating == True:
            self.WasteGeneratedTerytPk = self.wasteGeneratedTerytPk_entry.get("1.0", "end-1c") if hasattr(self,
                                                                                                          'wasteGeneratedTerytPk_entry') else None
            self.WasteGeneratingAdditionalInfo = self.wasteGeneratingAdditionalInfo_entry.get("1.0",
                                                                                              "end-1c") if hasattr(self,
                                                                                                                   'wasteGeneratingAdditionalInfo_entry') else None
        else:
            self.WasteGeneratedTerytPk = None
            self.WasteGeneratingAdditionalInfo = None

        data = {
                "KpoId": self.card_id_edit,
                "CertificateNumber": self.CertificateNumberAndBoxNumbers,
                "RealTransportTime": self.PlannedTransportTime,
                "WasteCodeId": self.WasteCodeId,
                "VehicleRegNumber": self.VehicleRegNumber,
                "WasteMass": self.replace_comma_with_dot(self.WasteMass),
                "PlannedTransportTime": self.PlannedTransportTime,
                "WasteProcessId": self.WasteProcessId,
                "AdditionalInfo": self.AdditionaInfo,
                "WasteCodeExtended": self.waste_code_extended,
                "WasteCodeExtendedDescription": self.WasteCodeExtendedDescription,
                "HazardousWasteReclassification": self.hazardous_waste_reclassification,
                "HazardousWasteReclassificationDescription": self.HazardousWasteReclassificationDescription,
                "IsWasteGenerating": self.is_waste_generating,
                "WasteGeneratedTerytPk": self.WasteGeneratedTerytPk,
                "WasteGeneratingAdditionalInfo": self.WasteGeneratingAdditionalInfo
                }

        return data


    @staticmethod
    def convert_datetime_to_iso_format(input_datetime_str):

        datetime_obj = datetime.strptime(input_datetime_str, '%Y-%m-%d %H:%M:%S')

        output_datetime_str = datetime_obj.isoformat() + "Z"

        return output_datetime_str


    def gather_all_data(self):
        self.CarrierCompanyId = self.carrier_company_id if hasattr(self, 'carrier_company_id') else None
        self.ReceiverCompanyId = self.receiver_company_id if hasattr(self, 'receiver_company_id') else None
        self.ReceiverEupId = self.EUP_ID if hasattr(self, 'EUP_ID') else None
        self.WasteCodeId = self.own_code if hasattr(self, 'own_code') else None
        self.VehicleRegNumber = self.vehicle_reg_number_entry.get() if hasattr(self,
                                                                               'vehicle_reg_number_entry') else None
        self.WasteMass = self.waste_mass_entry.get() if hasattr(self, 'waste_mass_entry') else None
        self.PrePlannedTransportTime = self.planned_transport_time_entry.get() if hasattr(self,
                                                                                          'planned_transport_time_entry') else None
        self.PlannedTransportTime = self.format_date(self.PrePlannedTransportTime) if hasattr(self,
                                                                                              'PrePlannedTransportTime') else None
        self.WasteProcessId = self.process_id if hasattr(self, 'process_id') else None
        self.CertificateNumberAndBoxNumbers = self.certificate_number_and_box_numbers_entry.get() if hasattr(self,
                                                                                                             'certificate_number_and_box_numbers_entry') else None
        self.AdditionaInfo = self.additional_info_entry.get("1.0", "end-1c") if hasattr(self,
                                                                                        'additional_info_entry') else None
        self.waste_code_extended = self.waste_code_extended_var.get() if hasattr(self,
                                                                                 'waste_code_extended_var') else None
        if self.waste_code_extended == True:
            self.WasteCodeExtendedDescription = self.waste_code_extended_description_entry.get("1.0",
                                                                                               "end-1c") if hasattr(
                self, 'waste_code_extended_description_entry') else None
        else:
            self.WasteCodeExtendedDescription = None
        self.hazardous_waste_reclassification = self.hazardous_waste_reclassification_var.get() if hasattr(self,
                                                                                                           'hazardous_waste_reclassification_var') else None
        if self.hazardous_waste_reclassification == True:
            self.HazardousWasteReclassificationDescription = self.hazardous_waste_reclassification_description_entry.get(
                "1.0", "end-1c") if hasattr(self, 'hazardous_waste_reclassification_description_entry') else None
        else:
            self.HazardousWasteReclassificationDescription = None
        self.is_waste_generating = self.is_waste_generating_var.get() if hasattr(self,
                                                                                 'is_waste_generating_var') else None
        if self.is_waste_generating == True:
            self.WasteGeneratedTerytPk = self.wasteGeneratedTerytPk_entry.get("1.0", "end-1c") if hasattr(self,
                                                                                                          'wasteGeneratedTerytPk_entry') else None
            self.WasteGeneratingAdditionalInfo = self.wasteGeneratingAdditionalInfo_entry.get("1.0",
                                                                                              "end-1c") if hasattr(self,
                                                                                                                   'wasteGeneratingAdditionalInfo_entry') else None
        else:
            self.WasteGeneratedTerytPk = None
            self.WasteGeneratingAdditionalInfo = None

        data = {
            "CarrierCompanyId": self.CarrierCompanyId,
            "ReceiverCompanyId": self.ReceiverCompanyId,
            "ReceiverEupId": self.ReceiverEupId,
            "WasteCodeId": self.WasteCodeId,
            "VehicleRegNumber": self.VehicleRegNumber,
            "WasteMass": self.replace_comma_with_dot(self.WasteMass),
            "PlannedTransportTime": self.PlannedTransportTime,
            "WasteProcessId": self.WasteProcessId,
            "CertificateNumberAndBoxNumbers": self.CertificateNumberAndBoxNumbers,
            "AdditionalInfo": self.AdditionaInfo,
            "WasteCodeExtended": self.waste_code_extended,
            "WasteCodeExtendedDescription": self.WasteCodeExtendedDescription,
            "HazardousWasteReclassification": self.hazardous_waste_reclassification,
            "HazardousWasteReclassificationDescription": self.HazardousWasteReclassificationDescription,
            "IsWasteGenerating": self.is_waste_generating,
            "WasteGeneratedTerytPk": self.WasteGeneratedTerytPk,
            "WasteGeneratingAdditionalInfo": self.WasteGeneratingAdditionalInfo
        }

        return data


    def save_data(self):
        try:
            if hasattr(self, 'child_window_receiver') and self.child_window_receiver is not None:
                self.child_window_receiver.destroy()
                self.child_window_receiver = None
            if hasattr(self, 'child_window_transmitter') and self.child_window_transmitter is not None:
                self.child_window_transmitter.destroy()
                self.child_window_transmitter = None
            if hasattr(self, 'child_window_transporter') and self.child_window_transporter is not None:
                self.child_window_transporter.destroy()
                self.child_window_transporter = None
        except Exception as e:
            print(f"Wystąpił błąd podczas zamykania okien: {e}")

        data = self.gather_all_data()

        response_data = KpoRequests.KPO().tworzenie_karty_ze_statusem_planowana(data, self.toplevel)
        if response_data:
            self.save_data_to_database()
        else:
            tk.messagebox.showerror("Błąd", "Nie udało się utworzyć karty planowanej w systemie zewnętrznym.")


    def open_calendar(self):
        self.calendar_window = tk.Toplevel()
        self.calendar_window.title("Wybierz datę i godzinę")

        self.cal = Calendar(self.calendar_window, selectmode='day', date_pattern='y-mm-dd', year=datetime.now().year,
                            month=datetime.now().month, day=datetime.now().day)
        self.cal.pack(pady=10, side='top')

        current_time = datetime.now()

        frame = tk.Frame(self.calendar_window)
        frame.pack()

        self.hour_var = tk.StringVar(value="{:02d}".format(current_time.hour))
        self.hour_label = ttk.Label(frame, text="Godzina:")
        self.hour_label.pack(side='left')
        self.hour_spinbox = ttk.Spinbox(frame, from_=0, to=23, width=5, format="%02.0f",
                                        textvariable=self.hour_var)
        self.hour_spinbox.pack(side='left')

        self.minute_var = tk.StringVar(value="{:02d}".format(current_time.minute))
        self.minute_label = ttk.Label(frame, text="Minuta:")
        self.minute_label.pack(side='left')
        self.minute_spinbox = ttk.Spinbox(frame, from_=0, to=59, width=5, format="%02.0f",
                                          textvariable=self.minute_var)
        self.minute_spinbox.pack(side='left')

        self.second_var = tk.StringVar(value="{:02d}".format(current_time.second))
        self.second_label = ttk.Label(frame, text="Sekunda:")
        self.second_label.pack(side='left')
        self.second_spinbox = ttk.Spinbox(frame, from_=0, to=59, width=5, format="%02.0f",
                                          textvariable=self.second_var)
        self.second_spinbox.pack(side='left')



        select_button = ttk.Button(self.calendar_window, text="Wybierz", command=self.save_date)
        select_button.pack(side='bottom', pady=10)


    def save_date(self):
        date = self.cal.get_date()
        hour = self.hour_spinbox.get()
        minute = self.minute_spinbox.get()
        second = self.second_spinbox.get()

        if hour == "" or minute == "":
            current_time = datetime.now()
            hour = current_time.strftime("%H")
            minute = current_time.strftime("%M")
            second = current_time.strftime("%S")

        full_date = f"{date} {hour}:{minute}:{second}"
        self.planned_transport_time_entry.delete(0, tk.END)
        self.planned_transport_time_entry.insert(0, full_date)
        self.calendar_window.destroy()

        if self.check_date(full_date):
            self.frame7.config(highlightbackground=self.highlightbackground, highlightcolor=self.highlightbackground)
            self.DateCorrect = True
        else:
            self.frame7.config(highlightbackground="red", highlightcolor="red")
            self.DateCorrect = False
            tk.messagebox.showerror("Błąd",
                                    "Format daty jest nieodpowiedni lub wybrana data nie znajduje się w zakresie 30 dni od daty dzisiejszej")

        self.check_fields()


    @staticmethod
    def check_date(date_str):

        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            current_date = datetime.now()
            if selected_date < current_date - timedelta(days=30) or selected_date > current_date + timedelta(days=30):
                return False
            return True
        except ValueError:
            return False


    @staticmethod
    def resize_and_display_image(image_path, new_size):
        original_image = Image.open(image_path)
        resized_image = original_image.resize(new_size)
        return ImageTk.PhotoImage(resized_image)


    def open_transporter_window(self, entry_target):
        if entry_target == "przewoznik":
            callback = self.receive_transporter_data
        else:
            callback = self.receive_receiver_data

        self.podmioty = SelectTransporterWindow.Transporter_window(callback)
        self.podmioty.window()


    def open_place_window(self):

        self.child_window_transporter = None
        self.child_window_receiver = None
        self.child_window_transmitter = None
        self.place_window = LocationSelection.Application(self.receive_place_data)
        self.place_window.create_widgets()


    def receive_place_data(self, data):

        self.my_place_entry.delete(0, tk.END)
        self.my_place_entry.insert(0, data[2])
        self.company_index = data[0]
        ApiConnection.Connection().access_attempt_with_auth(data[0])
        self.company_info()


    def open_receiver_window(self):
        self.podmioty = SelectTransporterWindow.Receiver_window(self.receive_receiver_data)
        self.podmioty.window()


    def open_teryt_window(self):
        self.teryt_data = SelectTransporterWindow.SelectTeryt(self.receive_teryt_code)
        self.teryt_data.window()


    def receive_teryt_code(self, data):
        self.teryt = data[0]
        self.wasteGeneratedTerytPk_entry.delete('1.0', tk.END)
        self.wasteGeneratedTerytPk_entry.insert('1.0', self.teryt)
        self.wasteGeneratedTerytPk_entry['state'] = 'disabled'


    def open_receiver_eup_window(self):
        self.podmioty = SelectTransporterWindow.Receiver_window(self.receive_receiver_eup_data)
        self.podmioty.window()


    def open_waste_window(self, callback):
        self.waste = SelectWasteWindow.WasteWindow(callback)
        self.waste.window()


    def receive_waste_code(self, code):
        self.waste_code_id_entry.delete(0, tk.END)
        self.own_code= self.waste_list.search_from_list(code)
        self.waste_code_id_entry.insert(0, code)


    def open_waste_prcoess_window(self, callback):
        self.waste = WasteProcessWindow.WasteProcessWindow(callback)
        self.waste.window()


    def receive_waste_process(self, code):
        self.process_id = code[0]
        code = code[2]
        self.waste_process_id_entry.delete(0, tk.END)
        self.waste_process_id_entry.insert(0, code)


    def receive_receiver_eup_data(self, data):
        self.dataCompany = data[1]
        self.dataCompanyEUP = data[0]
        self.EUP_ID = self.dataCompanyEUP[0]
        self.receiver_company_id = self.dataCompanyEUP[1]
        data = self.dataCompany[2]
        self.receiver_eup_id_entry.delete(0, tk.END)
        self.receiver_eup_id_entry.insert(0, data)


    def receive_transporter_data(self, data):
        self.carrier_company_id = data[0]
        data = data[2]
        self.carrier_company_entry.delete(0, tk.END)
        self.carrier_company_entry.insert(0, data)


    def receive_receiver_data(self, data):
        self.receiver_company_entry.delete(0, tk.END)
        self.receiver_company_entry.insert(0, data)


if __name__ == "__main__":

    StartWindow().Error_window()
