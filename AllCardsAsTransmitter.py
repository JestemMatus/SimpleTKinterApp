import tkinter as tk
from tkinter import ttk, messagebox
import os
import KpoRequests
import csv
from Globals import csv_transmitter_file, highlightbackground, highlightcolor
import CompanyLabel

class CardsListApplication():
    def __init__(self, callback=None):
        self.callback = callback
        self.topLevel = tk.Toplevel()
        self.topLevel.title('Waste Transport Data Viewer')
        self.topLevel.state("zoomed")
        self.page_data = KpoRequests.KPO()
        self.all_items = []
        self.csv_file_name = csv_transmitter_file
        self.create_widgets()

    def create_widgets(self):
        self.main_frame = tk.Frame(self.topLevel)
        self.main_frame.pack()

        self.frame_internal = tk.Frame(self.main_frame, highlightbackground=highlightbackground,
                                       highlightcolor=highlightcolor, highlightthickness=2)
        self.frame_internal.pack(pady=(10, 0))

        self.company = CompanyLabel.CompanyFrame(self.frame_internal, 0, 0, self.topLevel, 139)
        self.company.main_frame()

        self.tree_frame = tk.Frame(self.main_frame, highlightbackground=highlightbackground,
                                   highlightcolor=highlightcolor, highlightthickness=2)
        self.tree_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.tree_frame, show='headings', height=10)
        self.tree['columns'] = ('kpoId','plannedTransportTime', 'realTransportTime', 'wasteCode', 'wasteCodeDescription',
                                'vehicleRegNumber', 'cardStatus','cardNumber', 'senderName', 'receiverName')

        self.tree.heading('kpoId', text='Id_karty')
        self.tree.column('kpoId', width=0, minwidth=0, stretch=tk.NO)
        self.tree.heading('plannedTransportTime', text='Planowany czas transportu')
        self.tree.column('plannedTransportTime', width=110, anchor="center")
        self.tree.heading('realTransportTime', text='Rzeczywisty czas transportu')
        self.tree.column('realTransportTime', width=110, anchor="center")
        self.tree.heading('wasteCode', text='Kod')
        self.tree.column('wasteCode', width=50, anchor="center")
        self.tree.heading('wasteCodeDescription', text='Opis kodu odpadów')
        self.tree.column('wasteCodeDescription', width=200, anchor="center")
        self.tree.heading('vehicleRegNumber', text='Numer rejestracyjny pojazdu')
        self.tree.column('vehicleRegNumber', width=70, anchor="center")
        self.tree.heading('cardStatus', text='Status karty')
        self.tree.column('cardStatus', width=80, anchor="center")
        self.tree.heading('cardNumber', text='Numer karty')
        self.tree.column('cardNumber', width=200, anchor="center")
        self.tree.heading('senderName', text='Nazwa nadawcy')
        self.tree.column('senderName', width=205, anchor="center")
        self.tree.heading('receiverName', text='Nazwa odbiorcy')
        self.tree.column('receiverName', width=205, anchor="center")


        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tree_scroll = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.configure(yscrollcommand=self.tree_scroll.set)

        self.load_data_from_csv()

        self.tree.bind('<Double-1>', self.on_item_double_click)

        frame = tk.Frame(self.main_frame)
        frame.pack()

        self.details = ttk.Button(frame, text="Pokaż szczegóły", command=self.show_details)
        self.details.grid(row=0, column=1)

        self.topLevel.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.topLevel.mainloop()

    def on_closing(self):
        self.topLevel.destroy()

    def load_data_from_csv(self):
        if os.path.exists(self.csv_file_name):
            with open(self.csv_file_name, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.tree.insert("", tk.END, values=(
                    row['kpoId'], row['plannedTransportTime'].replace('T', ' '), row['realTransportTime'].replace('T', ' '), row['wasteCode'],
                    row['wasteCodeDescription'], row['vehicleRegNumber'], row['cardStatus'],row['cardNumber'], row['senderName'],
                    row['receiverName']))
                    self.all_items.append(
                        row)
        else:
            messagebox.showerror("Błąd", "Plik danych nie istnieje.")

    def confrim_card(self):
        selection = self.tree.selection()
        if selection:
            card_id = self.tree.item(selection, 'values')[0]
            result = self.page_data.zmiana_statusu_karty_z_planowanej_na_zatwierdzona(card_id,self.topLevel)
            if result:
                self.update_treeview_from_csv(card_id)
            else:
                self.update_treeview_from_csv(card_id)



    def delete_card(self):
        selection = self.tree.selection()
        if selection:
            card_id = self.tree.item(selection, 'values')[0]
            result = self.page_data.usuwanie_karty_ze_statusem_planowana(card_id, self.topLevel)
            if result:
                self.update_treeview_from_csv(card_id)
            else:
                self.update_treeview_from_csv(card_id)




    def update_treeview_from_csv(self, removed_id):

        new_data = []
        with open(self.csv_file_name, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader)
            for row in reader:
                if row[0] != removed_id:
                    new_data.append(row)

        for i in self.tree.get_children():
            self.tree.delete(i)

        for item in new_data:
            self.tree.insert('', 'end', values=item)


    def refresh_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

    def display_data(self, items):
        for item in items:
            self.tree.insert('', 'end', values=(
            item['kpoId'], item['plannedTransportTime'], item['realTransportTime'], item['wasteCode'],
            item['wasteCodeDescription'], item['vehicleRegNumber'], item['cardStatus'],
            item['senderName'], item['receiverName']))

    @staticmethod
    def save_data_to_csv(filename, data):
        headers = ['ID', 'Planned Transport Time', 'Real Transport Time', 'Waste Code', 'Waste Description',
                   'Vehicle Reg Number', 'Status', 'Sender Name', 'Receiver Name']

        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(data)

        print(f'Dane zostały zapisane do pliku {filename}.')

    def on_item_double_click(self, event):
        self.show_details()
        print(self.all_items)

    def show_details(self):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection, 'values')
            card_status = item[6]
            print(card_status)
            selected_id = item[0]

            if card_status == "Potwierdzenie wygenerowane":
                data = self.page_data.szczegoly_karty_wygenerowane_potwierdzenie(selected_id, 1)
            elif card_status == "Zatwierdzona":
                data = self.page_data.szczegoly_karty_zatwierdzona(selected_id, 1)
            elif card_status == "Odrzucona":
                data = self.page_data.szczegoly_karty_odrzucona(selected_id, 1)
            elif card_status == "Wycofana":
                data = self.page_data.szczegoly_karty_wycofana(selected_id, 1)
            elif card_status == "Potwierdzenie przejęcia":
                data = self.page_data.szczegoly_karty_wygenerowane_potwierdzone_przyjecie(selected_id, 1)
            elif card_status == "Potwierdzenie transportu":
                data = self.page_data.szczegoly_karty_potwierdzony_transport(selected_id, 1)
            elif card_status == "Planowana":
                data = self.page_data.szczegoly_karty_planowana(selected_id, 1)
            else:
                data = "BŁĄD"

            details_message = "Szczegóły transportu:\n\n" + "\n".join(
                f"{k}: {v}" for k, v in zip(self.tree['columns'], item))
            messagebox.showinfo("Szczegóły", details_message + str(data), parent=self.topLevel)



if __name__ == "__main__":
    app = CardsListApplication()
    app.create_widgets()
