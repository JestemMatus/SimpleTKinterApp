import tkinter as tk
from tkinter import ttk
import threading
import csv
import os
import KpoRequests
import time
from Globals import csv_transmitter_file


class CSVDataSaver:
    def __init__(self, progress_callback):
        self.page_data = KpoRequests.KPO()
        self.all_items = []
        self.progress_callback = progress_callback
        self.csv_transmitter_file = csv_transmitter_file

    def delete_data_file(self):
        try:
            os.remove(self.csv_transmitter_file)
            print("Plik "+(str(self.csv_transmitter_file))+" został usunięty.")
        except FileNotFoundError:
            print("Plik "+(str(self.csv_transmitter_file))+" nie istnieje, więc nie może być usunięty.")

    def load_data(self):
        if os.path.exists(self.csv_transmitter_file):
            os.remove(self.csv_transmitter_file)

        self.page_number = 1
        hasNextPage = True
        total_pages = 1

        try:
            with open('11TEST.csv', 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['kpoId', 'plannedTransportTime', 'realTransportTime', 'wasteCode', 'wasteCodeDescription',
                              'vehicleRegNumber', 'cardStatus', 'cardNumber', 'senderName', 'receiverName']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                while hasNextPage:
                    page_data = self.page_data.wyszukiwarka_kart(self.page_number, 50, 50)
                    if page_data and 'items' in page_data:
                        total_pages = page_data['totalPagesNumber']
                        for item in page_data['items']:
                            self.all_items.append(item)
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
                                'receiverName': item['receiverName'],

                            })
                        hasNextPage = page_data.get('hasNextPage', False)
                        if hasNextPage or self.page_number == total_pages:
                            self.progress_callback(self.page_number, total_pages)
                        self.page_number += 1
                    else:
                        print(f"Nie udało się załadować danych dla strony {self.page_number}.")
                        hasNextPage = False
        except Exception as e:
            print(f"Wystąpił błąd podczas zapisywania do pliku CSV: {e}")


class ProgressBarWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Postęp pobierania danych")

        self.progress = ttk.Progressbar(self.root, orient="horizontal",
                                        length=400, mode='determinate')
        self.progress.pack(pady=20)

        self.status_label = tk.Label(self.root, text="Rozpoczęto pobieranie danych...")
        self.status_label.pack(pady=10)

        threading.Thread(target=self.start_data_saver).start()

    def update_progress_bar(self, current, total):
        def _update():
            self.progress["maximum"] = total
            self.progress["value"] = current
            self.status_label.config(text=f"Pobieranie kart: {current} z {total}")
            if current == total:
                self.status_label.config(text="Pobieranie zakończone")
                self.root.after(1000, self.root.destroy)

        self.root.after(0, _update)

    @staticmethod
    def delete_data_file(filename):
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                os.remove(filename)
                print(f"Plik '{filename}' został usunięty.")
                break
            except PermissionError as e:
                print(f"Nie można usunąć pliku '{filename}', próba {attempt + 1}/{max_attempts}. Powód: {e}")
                time.sleep(1)

    def start_data_saver(self):
        try:
            data_saver = CSVDataSaver(self.update_progress_bar)
            data_saver.delete_data_file()
            data_saver.load_data()
        except Exception as e:
            print(f"Wystąpił wyjątek w start_data_saver: {e}")

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    ProgressBarWindow().run()
