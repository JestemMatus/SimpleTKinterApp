import tkinter as tk
from tkinter import ttk, messagebox
import os
import KpoRequests
import csv
import CompanyLabel
from Globals import csv_transmitter_file, highlightbackground, highlightcolor
from PdfCreator import PdfCreator

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
                                'vehicleRegNumber', 'cardStatus', 'cardNumber', 'senderName', 'receiverName')

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

        self.load_data()

        self.tree.bind('<Double-1>', self.on_item_double_click)

        frame = tk.Frame(self.main_frame)
        frame.pack()

        self.details = ttk.Button(frame, text="Pokaż szczegóły", command=self.show_details)
        self.details.grid(row=0, column=1)

        self.download_pdf = ttk.Button(frame, text="Wygeneruj pdf", command=self.generate_pdf)
        self.download_pdf.grid(row=0, column=2)


        self.topLevel.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.topLevel.mainloop()

    def generate_pdf(self):
        PdfCreator().gen_conf(self.tree,self.topLevel)

    def confirm_transport(self):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection, 'values')
            selected_id = item[0]
            result = KpoRequests.KPO().zmiana_statusus_na_potwierdzenie_transportu(selected_id, self.topLevel)
            if result:
                print("Błąd podczas zmiany statusu karty")
            else:
                self.update_csv_status(selected_id, 'Potwierdzenie transportu')
                self.update_treeview_from_csv()
                print("Status karty zaktualizowany pomyślnie")

    def on_closing(self):
        self.topLevel.destroy()

    def load_data(self):
        if os.path.exists(self.csv_file_name):
            with open(self.csv_file_name, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['cardStatus'] == 'Potwierdzenie przejęcia':
                        self.tree.insert("", tk.END, values=(
                            row['kpoId'], row['plannedTransportTime'].replace('T', ' '), row['realTransportTime'].replace('T', ' '), row['wasteCode'],
                            row['wasteCodeDescription'], row['vehicleRegNumber'],row['cardStatus'],row['cardNumber'] , row['senderName'],
                            row['receiverName']))
                        self.all_items.append(row)
        else:
            messagebox.showerror("Błąd", "Plik danych nie istnieje.", parent=self.topLevel)

    def on_item_double_click(self, event):
        self.show_details()
        print(self.all_items)


    def show_details(self):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection, 'values')
            selected_id = item[0]
            data = self.page_data.szczegoly_karty_wygenerowane_potwierdzone_przyjecie(selected_id,0)
            print(data)
            details_message = "Szczegóły transportu:\n\n" + "\n".join(f"{k}: {v}" for k, v in zip(self.tree['columns'], item))
            messagebox.showinfo("Szczegóły", details_message+str(data), parent=self.topLevel)

    def update_treeview_from_csv(self):

        for i in self.tree.get_children():
            self.tree.delete(i)

        self.load_data()

    def update_csv_after_deletion(self, card_id):
        updated_data = []
        with open(self.csv_file_name, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['kpoId'] != card_id:
                    updated_data.append(row)

        with open(self.csv_file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(updated_data)

        self.all_items = updated_data

    def update_csv_status(self, card_id, new_status):
        updated_data = []
        with open(self.csv_file_name, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['kpoId'] == card_id:
                    row['cardStatus'] = new_status
                updated_data.append(row)

        with open(self.csv_file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(updated_data)

        self.all_items = updated_data


if __name__ == "__main__":
    app = CardsListApplication()
    app.create_widgets()
