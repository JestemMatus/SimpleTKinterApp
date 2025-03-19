import tkinter as tk
from tkinter import ttk, messagebox
import os
import KpoRequests
import ApiConnection
import csv
from Globals import csv_receiver_file, highlightbackground, highlightcolor
import threading
import CompanyLabel
from BothStructure import CenterWindow
import time


class CardsListApplication():
    def __init__(self, company_index, callback = None):
        self.callback = callback
        self.all_items =[]
        self.company_index = company_index
        self.page_data = KpoRequests.KPO()
        self.csv_file_name = csv_receiver_file
        self.start_progress_and_save_data()
        print("To jest company index "+str(self.company_index))


    def setup_ui(self):
        self.topLevel = tk.Toplevel()
        self.topLevel.title('Waste Transport Data Viewer')
        self.topLevel.state("zoomed")
        self.create_widgets()


    def create_widgets(self):
        self.main_frame = tk.Frame(self.topLevel)
        self.main_frame.pack()

        self.frame_internal = tk.Frame(self.main_frame, highlightbackground=highlightbackground,
                                       highlightcolor=highlightcolor, highlightthickness=2)
        self.frame_internal.pack(pady=(10, 0))

        self.company = CompanyLabel.CompanyFrame(self.frame_internal, 0, 0, self.topLevel, 139)
        self.company.main_frame()

        self.tree_frame = tk.Frame(self.main_frame, highlightbackground=highlightbackground, highlightcolor=highlightcolor, highlightthickness=2)
        self.tree_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.tree_frame, show='headings', height=10)
        self.tree['columns'] = ('kpoId','plannedTransportTime', 'realTransportTime', 'wasteCode',
                                'wasteCodeDescription',
                                'vehicleRegNumber', 'cardStatus','cardNumber', 'senderName', 'receiverName')

        self.tree.heading('kpoId', text='Id_karty')
        self.tree.column('kpoId', width=0, minwidth=0, stretch=tk.NO,anchor="center")
        self.tree.heading('plannedTransportTime', text='Planowany czas transportu')
        self.tree.column('plannedTransportTime', width=115, anchor="center")
        self.tree.heading('realTransportTime', text='Rzeczywisty czas transportu')
        self.tree.column('realTransportTime', width=115, anchor="center")
        self.tree.heading('wasteCode', text='Kod')
        self.tree.column('wasteCode', width=50, anchor="center")
        self.tree.heading('wasteCodeDescription', text='Opis kodu odpadów')
        self.tree.column('wasteCodeDescription', width=160, anchor="center")
        self.tree.heading('vehicleRegNumber', text='Numer rejestracyjny pojazdu')
        self.tree.column('vehicleRegNumber', width=110, anchor="center")
        self.tree.heading('cardStatus', text='Status karty')
        self.tree.column('cardStatus', width=80, anchor="center")
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

        self.load_data_from_csv()

        self.tree.bind('<Double-1>', self.on_item_double_click)

        frame = tk.Frame(self.main_frame)
        frame.pack()

        self.finish_card_list = ttk.Button(frame, text="Wyświetl karty o statusie potwierdzony transport lub zrealizowane przejęcie", command=self.load_data_ptzp)
        self.finish_card_list.grid(row=0, column=3)
        self.reject_list_button = ttk.Button(frame, text="Wyświetl karty o statusie Odrzucona", command=self.reject_list_card)
        self.reject_list_button.grid(row=0, column=2)

        self.back_button = ttk.Button(frame, text="Powrót", command=self.back)
        self.back_button.grid(row=0, column=1)

        self.confirm_button = ttk.Button(frame, text="Potwierdź przejęcie", command=self.receiver_conf)
        self.confirm_button.grid(row=0, column=4)

        self.reject_button = ttk.Button(frame, text="Odrzuć", command=self.reject_card)
        self.reject_button.grid(row=0, column=5)

        self.reload_button = ttk.Button(frame, text="Odśwież dane", command=self.reload_data)
        self.reload_button.grid(row=0, column=0)

        self.topLevel.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.topLevel.mainloop()

    def reject_list_card(self):
        self.confirm_button.configure(state='disabled')
        self.reject_button.configure(state='disabled')
        self.refresh_data()
        self.load_data_from_csv("Odrzucona")

    def receiver_conf(self):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection, 'values')
            self.selected_id = item[0]
            data = self.page_data.szczegoly_karty_wygenerowane_potwierdzenie(self.selected_id, 0)
            WasteMass = data['wasteMass']
            self.toplevel3 = tk.Toplevel(self.topLevel)

            Correct_mass_label = ttk.Label(self.toplevel3, text="Skorygowana masa odpadu w tonach [Mg]: ")
            Correct_mass_label.grid(row=0, column=0)

            vcmd = (self.toplevel3.register(self.on_validate), '%P')

            self.Correct_mass_entry = ttk.Entry(self.toplevel3, width=8, validate='key', validatecommand=vcmd)
            self.Correct_mass_entry.grid(row=0, column=1)
            self.Correct_mass_entry.insert(0, WasteMass)

            Remarks_label = ttk.Label(self.toplevel3, text="Tu wpisz uwagi:")
            Remarks_label.grid(row=1, column=0, columnspan=2)

            self.Remarks_text = tk.Text(self.toplevel3, height=8, width=40)
            self.Remarks_text.grid(row=2, column=0, columnspan=2)

            frame = tk.Frame(self.toplevel3)
            frame.grid(row=3, column=0, columnspan=2)

            back_button = ttk.Button(frame, text="Anuluj", command=self.toplevel3.destroy)
            back_button.grid(row=0, column=0)

            confirm_button = ttk.Button(frame, text="Zatwierdź", command=self.confirm_card)
            confirm_button.grid(row=0, column=1)

            self.toplevel3.mainloop()

    def on_validate(self, value_if_allowed):
        if value_if_allowed == "":
            return True

        value_if_allowed = value_if_allowed.replace(',', '.')

        try:
            float_value = float(value_if_allowed)

            if value_if_allowed.count('.') > 1:
                return False

            parts = value_if_allowed.split('.')
            if len(parts) == 2 and len(parts[1]) > 4:
                return False

        except ValueError:
            return False

        return True

    def confirm_card(self):
        mass = self.Correct_mass_entry.get()
        remarks = self.Remarks_text.get("1.0","end-1c")
        kpo_id = self.selected_id
        result = KpoRequests.KPO().Zmiana_statusu_karty_z_wygenerowane_potwierdzenie_na_potwierdzenie_przyjecia(kpo_id,mass,remarks, self.toplevel3)
        if result:
            print("błąd")
        else:
            self.update_treeview_from_csv(kpo_id,"Potwierdzenie przejęcia", "Potwierdzenie wygenerowane")
        self.toplevel3.destroy()



    def reject_card(self):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection, 'values')
            selected_id = item[0]
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
                                                                                                      tk.END)))
            confirm_button.grid(row=0, column=1)
        else:
            pass

    def delete_card(self, card_id, remarks):
        if len(remarks) < 1:
            tk.messagebox.showerror("Błąd", "Wpisz powód odrzucenia karty.")
        else:
            result = self.page_data.zmiana_statusu_na_odrzucona(card_id, remarks, self.topLevel2)
            if result:
                print("Błąd")
            else:
                self.update_treeview_from_csv(card_id,"Odrzucona", "Potwierdzenie wygenerowane")
            self.topLevel2.destroy()

    def load_data_ptzp(self):
        self.refresh_data()
        self.load_data_from_csv("both")
        self.confirm_button.configure(state='disabled')
        self.reject_button.configure(state='disabled')


    def back(self):
        self.refresh_data()
        self.load_data_from_csv("Potwierdzenie wygenerowane")
        self.confirm_button.configure(state='normal')
        self.reject_button.configure(state='normal')

    def start_progress_and_save_data(self):
        def on_progress_finish():
            self.setup_ui()

        self.progress_window = ProgressBarWindow(self.company_index, on_progress_finish)
        self.progress_window.run()

    def load_data_from_csv(self, status_filters="Potwierdzenie wygenerowane"):
        if status_filters == "both":
            status_filters = ["Potwierdzenie transportu", "Potwierdzenie przejęcia"]

        self.all_items.clear()
        try:
            with open(self.csv_file_name, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['cardStatus'] in status_filters:
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

    def update_treeview_from_csv(self, card_id, new_status, old_status):
        updated_rows = []
        found = False
        try:
            with open(self.csv_file_name, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['kpoId'] == card_id:
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


    def refresh_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

    def on_closing(self):
        self.topLevel.withdraw()
        if self.callback:
            self.callback(self.topLevel)


    def on_item_double_click(self, event):
        self.show_details()

    def show_details(self):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection, 'values')
            selected_id = item[0]
            data = self.page_data.szczegoly_karty_zatwierdzona(selected_id,2)
            details_message = "Szczegóły transportu:\n\n" + "\n".join(f"{k}: {v}" for k, v in zip(self.tree['columns'], item))
            messagebox.showinfo("Szczegóły", details_message+str(data), parent=self.topLevel)

    def reload_data(self):
        self.topLevel.destroy()
        CardsListApplication(company_index=self.company_index)

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
                            page_data = self.page_data.wyszukiwarka_kart_przejmujacy(self.page_number, 50, False)
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
        self.csv_file = csv_receiver_file

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



if __name__ == "__main__":
    app = CardsListApplication(company_index=2)
