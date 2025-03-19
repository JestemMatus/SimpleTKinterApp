import tkinter as tk
from tkinter import ttk, messagebox
import threading
import csv
import os
from BothStructure import CenterWindow
import KpoRequests
import ApiConnection
from Globals import csv_transmitter_file
import time

class CardStatusWindow:
    def __init__(self, container, company_index, callback, parent_window):
        self.container = container

        self.data = [{'CardStatusId': 1, 'Name': 'Planowana', 'CodeName': 'PLANNED'}, {'CardStatusId': 2, 'Name': 'Zatwierdzona', 'CodeName': 'APPROVED'}, {'CardStatusId': 3, 'Name': 'Wycofana', 'CodeName': 'WITHDRAWN'}, {'CardStatusId': 4, 'Name': 'Potwierdzenie transportu', 'CodeName': 'TRANSPORT_CONFIRMATION'}, {'CardStatusId': 5, 'Name': 'Potwierdzenie wygenerowane', 'CodeName': 'CONFIRMATION_GENERATED'}, {'CardStatusId': 6, 'Name': 'Odrzucona', 'CodeName': 'REJECTED'}, {'CardStatusId': 7, 'Name': 'Potwierdzenie przejęcia', 'CodeName': 'RECEIVE_CONFIRMATION'}]
        self.callback = callback
        self.parent_window = parent_window
        self.planned = self.data[0]
        self.approved = self.data[1]
        self.withdrawn = self.data[2]
        self.transport_confirmation = self.data[3]
        self.confirmation_generated = self.data[4]
        self.rejected = self.data[5]
        self.receive_confirmation = self.data[6]
        self.company_index = company_index

    def retest(self):
        self.topLevelintermediate.destroy()
        ProgressBarWindow(self.company_index, callback=self.window).run()

    def test(self):
        ProgressBarWindow(self.company_index, callback=self.window).run()

    def window(self):
        self.topLevelintermediate = tk.Toplevel()

        main_container = tk.Frame(self.topLevelintermediate, width=900, height=500, bg='white')
        main_container.pack_propagate(False)
        main_container.grid(row=1, column=1, sticky='nswe')

        second_container = tk.Frame(main_container, background="white")
        second_container.pack_propagate(False)
        second_container.grid(row=2, column=1, sticky='nswe', pady=5, padx=15)

        self.button_planned = ttk.Button(second_container, text="Planowana", width=30,
                                         command=self.next_planned)
        self.button_planned.grid(row=1, column=0)
        self.button_approved = ttk.Button(second_container, text="Zatwierdzona", width=30, command=self.next_confirmed)
        self.button_approved.grid(row=1, column=1)
        self.button_withdrawn = ttk.Button(second_container, text="Wycofana", width=30, command=self.next_removed)
        self.button_withdrawn.grid(row=2, column=2)
        self.button_transport_confirmation = ttk.Button(second_container, text="Potwierdzenie transportu", width=30, command=self.next_transport_confirmed)
        self.button_transport_confirmation.grid(row=2, column=0)
        self.button_confirmation_generated = ttk.Button(second_container, text="Potwierdzenie wygenerowane", width=30, command=self.next_approved)
        self.button_confirmation_generated.grid(row=1, column=2)
        self.button_rejected = ttk.Button(second_container, text="Odrzucona", width=30, command=self.next_rejected)
        self.button_rejected.grid(row=2, column=3)
        self.button_receive_confirmation = ttk.Button(second_container, text="Potwierdzenie przejęcia", width=30, command=self.next_complited_transport)
        self.button_receive_confirmation.grid(row=1, column=3)
        self.button_all = ttk.Button(second_container, text="Wszystkie", width=30,
                                     command=self.next_all)
        self.button_all.grid(row=2,column=1)

        style = ttk.Style()
        style.configure('Large.TButton', font=('Arial', 10))

        self.button_refresh = ttk.Button(second_container, text="Odśwież wszystkie dane", width=50, command=self.retest, style='Large.TButton')
        self.button_refresh.grid(row=3, column=1, columnspan=2, pady=10, ipady=2)


        self.tree = ttk.Treeview(second_container, columns=('CardStatusId', 'Name', 'CodeName'), style="mystyle.Treeview", height=7)

        self.tree.heading('#0', text='', anchor="center")
        self.tree.heading('CardStatusId', text='#', anchor="center")
        self.tree.heading('Name', text='Typ karty', anchor="center")
        self.tree.heading('CodeName', text='Card Type', anchor="center")

        self.tree.column('#0', stretch=tk.NO, minwidth=0, width=0, anchor="center")
        self.tree.column('CardStatusId', stretch=tk.NO, minwidth=0, width=40, anchor="center")
        self.tree.column('Name', stretch=tk.NO, minwidth=0, width=350, anchor="w")
        self.tree.column('CodeName', stretch=tk.NO, minwidth=0, width=350, anchor="w")

        for item in self.data:
            self.tree.insert('', 'end', values=(item['CardStatusId'], item['Name'], self.format_string(item['CodeName'])))

        self.tree.grid(row=0,column=0, columnspan=12, sticky='n', pady=10)

        self.tree.bind('<Double-1>', self.double_click)

        self.topLevelintermediate.protocol("WM_DELETE_WINDOW", self.on_closing)

        CenterWindow().center_window(self.topLevelintermediate)
        self.topLevelintermediate.mainloop()

    def on_closing(self):
        self.topLevelintermediate.withdraw()
        if self.callback:
            self.callback("Brak",self.topLevelintermediate)

    @staticmethod
    def format_string(input_string):
        formatted_string = input_string.replace('_', ' ')
        return formatted_string[0].upper() + formatted_string[1:].lower()

    def double_click(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection, 'values')[0]
            if item == "1":
                self.next_planned()
            if item == "2":
                self.next_confirmed()
            if item == "3":
                self.next_removed()
            if item == "5":
                self.next_approved()
            if item == "7":
                self.next_complited_transport()
            if item == "6":
                self.next_rejected()
            if item == "4":
                self.next_transport_confirmed()
            else:
                pass

    def next_transport_confirmed(self):
        self.callback("Potwierdzony transport", self.topLevelintermediate)

    def next_rejected(self):
        self.callback('Odrzucona', self.topLevelintermediate)

    def next_complited_transport(self):
        self.callback('Potwierdzenie przejęcia', self.topLevelintermediate)

    def next_approved(self):
        self.callback('Potwierdzenie wygenerowane', self.topLevelintermediate)

    def next_confirmed(self):
        self.callback('Potwierdzona', self.topLevelintermediate)

    def next_planned(self):
        self.callback('Planowana', self.topLevelintermediate)

    def next_removed(self):
        self.callback('Wycofana', self.topLevelintermediate)

    def next_all(self):
        self.callback('Wszystkie', self.topLevelintermediate)


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
                            page_data = self.page_data.wyszukiwarka_kart(self.page_number, 50, False)

                            if page_data and 'items' in page_data and page_data['items']:
                                break
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
        self.csv_file = csv_transmitter_file

        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=400, mode='determinate')
        self.progress.pack(pady=20)

        self.status_label = tk.Label(self.root, text="Rozpoczęto pobieranie danych...")
        self.status_label.pack(pady=10)

        initial_data = self.page_data.wyszukiwarka_kart_transportujacy(1, 50,
                                                        True)

        self.elements = initial_data['totalPagesNumber']

        threading.Thread(target=self.start_data_saver).start()

        CenterWindow().center_window(self.root)

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
