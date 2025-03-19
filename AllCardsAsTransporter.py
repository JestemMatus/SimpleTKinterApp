import tkinter as tk
from tkinter import ttk, messagebox
import os
import time
import BothStructure
import KpoRequests
import ApiConnection
import csv
import threading
from datetime import datetime
from PdfCreator import PdfCreator
from Globals import csv_transporter_file, highlightcolor, highlightbackground
import CompanyLabel


class CardsListApplication:
    def __init__(self, company_index , callback = None):
        self.company_index = company_index
        self.callback = callback
        self.page_data = KpoRequests.KPO()
        self.csv_file_name = csv_transporter_file
        self.all_items = []
        self.active_button = None

        self.start_progress_and_save_data()

    def start_progress_and_save_data(self):
        def on_progress_finish():
            self.setup_ui()
            self.load_data_from_csv("Potwierdzenie przejęcia")

        self.progress_window = ProgressBarWindow(self.company_index, on_progress_finish)
        self.progress_window.run()

    def setup_ui(self):
        self.topLevel = tk.Toplevel()
        self.topLevel.title('Podmiot transportujący')
        self.topLevel.state('zoomed')
        self.create_widgets()

    def load_data_from_csv(self, status_filter="Potwierdzenie przejęcia"):
        self.confirm_transport_button.configure(state="disabled")
        self.all_items.clear()
        try:
            with open(self.csv_file_name, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['cardStatus'] == status_filter:
                        self.all_items.append(row)
                        card_number = row.get('cardNumber', 'Brak numeru')
                        self.tree.insert('', 'end', values=(
                            row['kpoId'], row['plannedTransportTime'].replace("T", " "),
                            row['realTransportTime'].replace("T", " "),
                            row['wasteCode'], row['wasteCodeDescription'], row['vehicleRegNumber'],
                            row['cardStatus'], card_number, row['senderName'], row['receiverName']))

        except Exception as e:
            messagebox.showerror("Błąd", f"Nie można załadować danych z pliku CSV: {e}")

    def load_data_with_progress(self):
        ProgressBarWindow(self.company_index, self.load_data_from_csv).run()

    def create_widgets(self):
        self.main_frame = tk.Frame(self.topLevel)
        self.main_frame.pack()

        self.frame_internal = tk.Frame(self.main_frame, highlightbackground=highlightbackground, highlightcolor=highlightcolor, highlightthickness=2)
        self.frame_internal.pack(pady=(10,0))

        self.company = CompanyLabel.CompanyFrame(self.frame_internal, 0, 0, self.topLevel, 139)
        self.company.main_frame()

        self.tree_frame = tk.Frame(self.main_frame, highlightbackground=highlightbackground, highlightcolor=highlightcolor, highlightthickness=2)
        self.tree_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.tree_frame, show='headings', height=10)
        self.tree['columns'] = ('kpoId','plannedTransportTime', 'realTransportTime', 'wasteCode', 'wasteCodeDescription',
                                'vehicleRegNumber', 'cardStatus','cardNumber', 'senderName', 'receiverName')

        self.tree.heading('kpoId', text='Id_karty')
        self.tree.column('kpoId', width=0, minwidth=0, stretch=tk.NO, anchor="center")
        self.tree.heading('plannedTransportTime', text='Planowany czas transportu')
        self.tree.column('plannedTransportTime', width=120, anchor="center")
        self.tree.heading('realTransportTime', text='Rzeczywisty czas transportu')
        self.tree.column('realTransportTime', width=120, anchor="center")
        self.tree.heading('wasteCode', text='Kod')
        self.tree.column('wasteCode', width=60, anchor="center")
        self.tree.heading('wasteCodeDescription', text='Opis kodu odpadów')
        self.tree.column('wasteCodeDescription', width=170, anchor="center")
        self.tree.heading('vehicleRegNumber', text='Numer rejestracyjny pojazdu')
        self.tree.column('vehicleRegNumber', width=60, anchor="center")
        self.tree.heading('cardStatus', text='Status karty')
        self.tree.column('cardStatus', width=100, anchor="center")
        self.tree.heading('cardNumber', text='Numer karty')
        self.tree.column('cardNumber', width=200, anchor="center")
        self.tree.heading('senderName', text='Nazwa nadawcy')
        self.tree.column('senderName', width=200, anchor="center")
        self.tree.heading('receiverName', text='Nazwa odbiorcy')
        self.tree.column('receiverName', width=200, anchor="center")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tree_scroll = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.configure(yscrollcommand=self.tree_scroll.set)


        self.tree.bind('<Double-1>', self.on_item_double_click)

        frame = tk.Frame(self.main_frame)
        frame.pack()

        width = 35

        frame_card_external = tk.Frame(frame, highlightbackground=highlightbackground, highlightcolor=highlightcolor, highlightthickness=2)
        frame_card_external.grid(row=0, column=0)

        frame_card_type = tk.Frame(frame_card_external)
        frame_card_type.grid(row=0, column=0, padx=30, pady=10)

        desc_label = ttk.Label(frame_card_type, text="Wybierz typ karty:")
        desc_label.grid(row=0, column=0, pady=(0,10))

        frame_actions_external = tk.Frame(frame, highlightbackground=highlightbackground, highlightcolor=highlightcolor, highlightthickness=2)
        frame_actions_external.grid(row=0, column=1, padx=10, sticky='n')

        frame_actions = tk.Frame(frame_actions_external)
        frame_actions.grid(row=0, column=0, padx=30, pady=10)

        self.details = ttk.Button(frame_actions, text="Pokaż szczegóły", width= width, command=self.show_details)
        self.details.grid(row=0, column=0)

        self.confirm_transport_button = ttk.Button(frame_actions, text="Potwierdź kartę",width= width, command=self.confrim_transport)
        self.confirm_transport_button.grid(row=0, column=3)

        self.confirm_button = ttk.Button(frame_actions, text="Potwierdź transport",width= width, command=self.receiver_conf)
        self.confirm_button.grid(row=0, column=2)

        self.reset_data_button = ttk.Button(frame_actions, text="Odśwież dane", width=width, command=self.reload_data)
        self.reset_data_button.grid(row=0, column=1)


        self.pdf_button = ttk.Button(frame_actions, text="Wygeneruj kartę PDF", width=72, command= self.pdf_create)
        self.pdf_button.grid(row=1, column=0, columnspan=2)

        self.pdf_button_conf = ttk.Button(frame_actions, text="Wygeneruj potwierdzenie PDF", width=72, command=self.pdf_confirm_create)
        self.pdf_button_conf.grid(row=1, column=2, columnspan=2)
        self.pdf_button_conf.configure(state="disabled")

        self.confirmed_cards = ttk.Button(frame_card_type, text="Zatwierdzona",width= width, command=lambda: self.planned_card_list("Zatwierdzona"))
        self.confirmed_cards.grid(row=1, column=0)

        self.confirm_generated_cards = ttk.Button(frame_card_type,width= width, text="Potwierdzenie wygenerowane",
                                 command=lambda: self.planned_card_list("Potwierdzenie wygenerowane"))
        self.confirm_generated_cards.grid(row=2, column=0)

        self.removed_cards = ttk.Button(frame_card_type, text="Wycofana",width= width,
                                                  command=lambda: self.planned_card_list("Wycofana"))
        self.removed_cards.grid(row=5, column=0)

        self.rejected_cards = ttk.Button(frame_card_type, text="Odrzucona",width= width,
                                        command=lambda: self.planned_card_list("Odrzucona"))
        self.rejected_cards.grid(row=6, column=0)

        self.complited_transport = ttk.Button(frame_card_type, text="Potwierdzenie przejęcia",width= width,
                                         command=lambda: self.planned_card_list("Potwierdzenie przejęcia"))
        self.complited_transport.grid(row=3, column=0)

        self.confirmed_transport = ttk.Button(frame_card_type, text="Potwierdzenie transportu",width= width,
                                              command=lambda: self.planned_card_list("Potwierdzenie transportu"))
        self.confirmed_transport.grid(row=4, column=0)

        self.all_cards_button = ttk.Button(frame_card_type, text="Wszystkie",width= width,
                                              command=self.all_cards_list)
        self.all_cards_button.grid(row=7, column=0)



        self.topLevel.protocol("WM_DELETE_WINDOW", self.on_closing)

    def reload_data(self):
        self.topLevel.destroy()
        CardsListApplication(company_index=self.company_index)


    def reject_card(self):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection, 'values')
            selected_id = item[0]
            time = item[2]
            reg = item[5]
            self.topLevel2 = tk.Toplevel(self.topLevel)
            self.topLevel2.geometry('600x200')
            remark_label = ttk.Label(self.topLevel2, text="Podaj powód wycofania karty:")
            remark_label.pack()
            remark_textbox = tk.Text(self.topLevel2, height=8)
            remark_textbox.pack()

            frame = tk.Frame(self.topLevel2)
            frame.pack()

            back_button = ttk.Button(frame, text="Anuluj", command=self.topLevel2.destroy)
            back_button.grid(row=0, column=0)

            confirm_button = ttk.Button(frame, text="Potwierdź", command=lambda: self.delete_card(selected_id,
                                                                                                  remark_textbox.get(
                                                                                                      "1.0",
                                                                                                      tk.END),time,reg))
            confirm_button.grid(row=0, column=1)
        else:
            messagebox.showerror("Błąd", "Nie wybrano karty")

    def delete_card(self, card_id, remarks, time, reg):
        if len(remarks) < 1:
            tk.messagebox.showerror("Błąd", "Wpisz powód odrzucenia karty.")
        else:
            result = self.page_data.zmiana_statusu_na_odrzucona(card_id, remarks, self.topLevel2)
            if result:
                print("Błąd")
            else:
                self.update_treeview_from_csv(card_id,"Odrzucona", "Potwierdzenie wygenerowane",time, reg)
            self.topLevel2.destroy()

    def pdf_confirm_create(self):
        PdfCreator().gen_conf_card(self.tree, self.topLevel)

    def pdf_create(self):
        PdfCreator().gen_conf(self.tree, self.topLevel)

    def all_cards_list(self):
        self.highlight_button("Wszystkie")
        self.confirm_transport_button.configure(state="disabled")
        self.confirm_button.configure(state="disabled")
        for i in self.tree.get_children():
            self.tree.delete(i)
        try:
            with open(self.csv_file_name, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    card_number = 'Brak numeru' if row['cardNumber'] is None else row['cardNumber']
                    self.tree.insert('', 'end', values=(
                        row['kpoId'], row['plannedTransportTime'].replace("T", " "),
                        row['realTransportTime'].replace("T", " "),
                        row['wasteCode'], row['wasteCodeDescription'], row['vehicleRegNumber'],
                        row['cardStatus'], card_number, row['senderName'], row['receiverName']))
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie można załadować danych z pliku CSV: {e}")

    def planned_card_list(self, card_name):
        self.highlight_button(card_name)
        for i in self.tree.get_children():
            self.tree.delete(i)

        try:
            with open(self.csv_file_name, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['cardStatus'] == card_name:
                        self.tree.insert('', 'end', values=(
                            row['kpoId'], row['plannedTransportTime'].replace("T", " "), row['realTransportTime'].replace("T", " "),
                            row['wasteCode'], row['wasteCodeDescription'], row['vehicleRegNumber'],
                            row['cardStatus'],row['cardNumber'] ,row['senderName'], row['receiverName']))
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie można załadować danych z pliku CSV: {e}")

        if card_name == "Potwierdzenie przejęcia":
            self.confirm_button.configure(state="normal")
        else:
            self.confirm_button.configure(state="disabled")

        if card_name == "Planowana":
            self.pdf_button.configure(state="disabled")
        else:
            self.pdf_button.configure(state="normal")

        if card_name == "Potwierdzenie wygenerowane":
            self.pdf_button_conf.configure(state="normal")
        else:
            self.pdf_button_conf.configure(state="disabled")

        if card_name == "Zatwierdzona":
            self.confirm_transport_button.configure(state="normal")
        else:
            self.confirm_transport_button.configure(state="disabled")

    def highlight_button(self, status):
        buttons = [
            self.confirmed_cards,
            self.confirm_generated_cards,
            self.removed_cards,
            self.rejected_cards,
            self.complited_transport,
            self.confirmed_transport,
            self.all_cards_button
        ]

        for button in buttons:
            button.state(['!pressed'])

        if status == "Planowana":
            pass
        elif status == "Zatwierdzona":
            self.confirmed_cards.state(['pressed'])
        elif status == "Potwierdzenie wygenerowane":
            self.confirm_generated_cards.state(['pressed'])
        elif status == "Potwierdzenie przejęcia":
            self.complited_transport.state(['pressed'])
        elif status == "Potwierdzenie transportu":
            self.confirmed_transport.state(['pressed'])
        elif status == "Wszystkie":
            self.all_cards_button.state(['pressed'])
        elif status == "Wycofana":
            self.removed_cards.state(['pressed'])
        elif status == "Odrzucona":
            self.rejected_cards.state(['pressed'])

        self.active_button = status

    def confrim_transport(self):
        selection = self.tree.selection()
        if selection:
            card_id = self.tree.item(selection, 'values')[0]
            veh_number = self.tree.item(selection, 'values')[5]
            real_time = self.tree.item(selection, 'values')[2]

            self.toplevel3 = tk.Toplevel(self.topLevel)

            real_transport_time = ttk.Label(self.toplevel3, text="Faktyczny czas rozpoczęcia transportu: ")
            real_transport_time.grid(row=0, column=0)

            self.real_transport_date = ttk.Entry(self.toplevel3, width=20)
            self.real_transport_date.grid(row=0, column=1)
            self.real_transport_date.insert(0, real_time)

            Reg_label = ttk.Label(self.toplevel3, text="Numer rejestracyjny pojazdu:")
            Reg_label.grid(row=1, column=0, columnspan=2)

            self.reg_entry = ttk.Entry(self.toplevel3, width=20)
            self.reg_entry.grid(row=2, column=0, columnspan=2)
            self.reg_entry.insert(0,veh_number)

            frame = tk.Frame(self.toplevel3)
            frame.grid(row=3, column=0, columnspan=2)

            back_button = ttk.Button(frame, text="Anuluj", command=self.toplevel3.destroy)
            back_button.grid(row=0, column=0)

            confirm_button = ttk.Button(frame, text="Zatwierdź", command=lambda: self.run_conf(card_id))
            confirm_button.grid(row=0, column=1)

            self.toplevel3.mainloop()

    @staticmethod
    def convert_datetime_to_iso_format(input_datetime_str):
        datetime_obj = datetime.strptime(input_datetime_str, '%Y-%m-%d %H:%M:%S')

        output_datetime_str = datetime_obj.isoformat() + "Z"

        return output_datetime_str

    def run_conf(self, card_id):
        data = self.page_data.szczegoly_karty_zatwierdzona(card_id, 0)

        vehNumber = self.reg_entry.get()
        print(vehNumber)
        RealTransportTime = self.convert_datetime_to_iso_format(self.real_transport_date.get())
        print(RealTransportTime)
        datetime_str = self.real_transport_date.get()
        datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        RealTransportHour = datetime_obj.strftime('%H:%M:%S')

        print(RealTransportHour)

        data2 = {
            "KpoId": card_id,
            "WasteCodeId": data['wasteCodeId'],
            "WasteProcessId": data['wasteProcessId'],
            "WasteMass": data['wasteMass'],
            "VehicleRegNumber": vehNumber,
            "CertificateNumber": data['certificateNumberAndBoxNumbers'],
            "PlannedTransportTime": data['plannedTransportTime'],
            "RealTransportTime": RealTransportTime,
            "AdditionalInfo": data['additionalInfo'],
            "WasteCodeExtended": data['wasteCodeExtended'],
            "WasteCodeExtendedDescription": data['wasteCodeExtendedDescription'],
            "HazardousWasteReclassification": data['hazardousWasteReclassification'],
            "HazardousWasteReclassificationDescription": data['hazardousWasteReclassificationDescription'],
            "IsWasteGenerating": data['isWasteGenerating'],
            "WasteGeneratedTerytPk": data['wasteGeneratedTerytPk'],
            "WasteGeneratingAdditionalInfo": data['wasteGeneratingAdditionalInfo']
        }

        self.page_data.wygeneruj_potwierdzenie(card_id,vehNumber, RealTransportHour, RealTransportTime, data2, self.toplevel3)
        self.update_treeview_from_csv(card_id, "Potwierdzenie wygenerowane", "Zatwierdzona",RealTransportTime, vehNumber)
        self.toplevel3.destroy()

    def update_treeview_from_csv(self, card_id, new_status, old_status, new_time, new_reg):
        updated_rows = []
        found = False
        try:
            with open(self.csv_file_name, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['kpoId'] == card_id:
                        row['realTransportTime'] = new_time
                        row['vehicleRegNumber'] = new_reg
                        row['cardStatus'] = new_status
                        found = True
                    updated_rows.append(row)

            if found:
                with open(self.csv_file_name, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
                    writer.writeheader()
                    writer.writerows(updated_rows)

                for i in self.tree.get_children():
                    self.tree.delete(i)

                self.load_data_from_csv(old_status)

            else:
                messagebox.showwarning("Błąd", "Nie znaleziono karty o podanym ID.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie można zaktualizować danych: {e}")

    def receiver_conf(self):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection, 'values')
            self.selected_id = item[0]
            time = item[2]
            reg = item[5]
            self.page_data.zmiana_statusus_na_potwierdzenie_transportu(self.selected_id, self.topLevel)
            self.update_treeview_from_csv(self.selected_id,"Potwierdzenie transportu", "Potwierdzenie przejęcia", time, reg)

    def on_closing(self):
        self.topLevel.withdraw()
        if self.callback:
            self.callback(self.topLevel)

    def refresh_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

    def on_item_double_click(self, event):
        self.show_details()

    def show_details(self):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection, 'values')
            card_status = item[6]
            selected_id = item[0]

            if card_status == "Potwierdzenie wygenerowane":
                data = self.page_data.szczegoly_karty_wygenerowane_potwierdzenie(selected_id,1)
            elif card_status == "Zatwierdzona":
                data = self.page_data.szczegoly_karty_zatwierdzona(selected_id,1)
            elif card_status =="Odrzucona":
                data = self.page_data.szczegoly_karty_odrzucona(selected_id,1)
            elif card_status =="Wycofana":
                data = self.page_data.szczegoly_karty_wycofana(selected_id,1)
            elif card_status =="Potwierdzenie przejęcia":
                data = self.page_data.szczegoly_karty_wygenerowane_potwierdzone_przyjecie(selected_id,1)
            elif card_status =="Potwierdzenie transportu":
                data = self.page_data.szczegoly_karty_potwierdzony_transport(selected_id,1)
            elif card_status =="Planowana":
                data = self.page_data.szczegoly_karty_planowana(selected_id,1)
            else:
                data = "BŁĄD"

            details_message = "Szczegóły transportu:\n\n" + "\n".join(f"{k}: {v}" for k, v in zip(self.tree['columns'], item))
            messagebox.showinfo("Szczegóły", details_message+str(data), parent=self.topLevel)

class CSVDataSaver:
    def __init__(self, progress_callback, csv_file):
        self.page_data = KpoRequests.KPO()
        self.progress_callback = progress_callback
        self.csv_file = csv_file

    def load_data(self):
        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)

        self.page_number = 1
        hasNextPage = True
        max_retries = 5
        retry_delay = 0.5

        try:
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['kpoId', 'plannedTransportTime', 'realTransportTime', 'wasteCode', 'wasteCodeDescription',
                              'vehicleRegNumber', 'cardStatus', 'cardNumber', 'senderName', 'receiverName']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                while hasNextPage:
                    page_data = None
                    retries = 0
                    while retries < max_retries:
                        try:
                            page_data = self.page_data.wyszukiwarka_kart_transportujacy(self.page_number, 50, False)
                            if page_data and 'items' in page_data and page_data['items']:
                                breaky
                            else:
                                raise Exception("Odpowiedź API nie zawiera danych.")
                        except Exception as error:
                            print(
                                f"Błąd przy pobieraniu danych strony {self.page_number}: {error}. Ponawianie próby {retries + 1}/{max_retries}.")
                            time.sleep(retry_delay)
                            retries += 1

                    if retries == max_retries:
                        print(f"Nie udało się pobrać danych strony {self.page_number} po {max_retries} próbach.")
                        break

                    for item in page_data['items']:
                        writer.writerow({
                            'kpoId': item['kpoId'],
                            'plannedTransportTime': item['plannedTransportTime'],
                            'realTransportTime': item['realTransportTime'],
                            'wasteCode': item['wasteCode'],
                            'wasteCodeDescription': item['wasteCodeDescription'],
                            'vehicleRegNumber': item['vehicleRegNumber'],
                            'cardStatus': item['cardStatus'],
                            'cardNumber': item['cardNumber'],
                            'senderName': item['senderName'],
                            'receiverName': item['receiverName']
                        })

                    hasNextPage = page_data.get('hasNextPage', False)
                    self.page_number += 1
                    self.progress_callback(self.page_number, page_data.get('totalPagesNumber', 0) + 1,
                                           "Pobieranie danych...")
        except Exception as e:
            print(f"Wystąpił błąd podczas zapisywania do pliku CSV: {e}")

class ProgressBarWindow:
    def __init__(self, company_index, callback=None):
        self.callback = callback
        self.company_index = company_index
        self.root = tk.Tk()
        self.root.title("Postęp pobierania danych")
        self.page_data = KpoRequests.KPO()
        self.csv_file = csv_transporter_file

        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=400, mode='determinate')
        self.progress.pack(pady=20)

        self.status_label = tk.Label(self.root, text="Rozpoczęto pobieranie danych...")
        self.status_label.pack(pady=10)

        initial_data = self.page_data.wyszukiwarka_kart_transportujacy(1, 50,
                                                        True)

        self.elements = initial_data['totalPagesNumber']

        threading.Thread(target=self.start_data_saver).start()

        BothStructure.CenterWindow().center_window(self.root)



    def update_progress_bar(self, current, total, status_text=""):
        self.root.after(0, lambda: self._update_progress_bar(current, total, status_text))

    def finish_progress(self):
        if not self.root.winfo_exists():
            return
        self.root.destroy()
        if self.callback:
            self.callback()

    def start_data_saver(self):
        self.update_progress_bar(0, 1, "Uzyskiwanie dostępu do bazy danych...")
        try:
            ApiConnection.Connection().access_attempt_with_auth(self.company_index)
            self.update_progress_bar(1, 2)
            data_saver = CSVDataSaver(lambda current, total, status_text="": self.update_progress_bar(current, total, status_text), self.csv_file)
            data_saver.load_data()
        except Exception as e:
            print(f"Wystąpił wyjątek: {e}")
            self.finish_progress()

    def _update_progress_bar(self, current, total, status_text=""):
        if not self.root.winfo_exists():
            return
        if total == 0:
            messagebox.showinfo("Informacja", "Brak danych do pobrania.")
            self.finish_progress()
            return
        self.progress["maximum"] = total
        self.progress["value"] = current
        self.status_label.config(text=status_text if status_text else f"Pobieranie danych: {current} z {total}")
        if current >= total:
            self.status_label.config(text="Pobieranie zakończone")
            self.root.after(500, self.finish_progress)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = CardsListApplication(company_index=1)