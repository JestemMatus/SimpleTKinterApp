import tkinter as tk
from tkinter import ttk, messagebox
import os
import KpoRequests
import csv
from Globals import csv_transmitter_file, highlightcolor, highlightbackground
from PdfCreator import PdfCreator
import CompanyLabel

class CardsListApplication():
    def __init__(self, inter_window ,callback=None):
        self.inter_window = inter_window
        self.callback = callback
        self.topLevel = tk.Toplevel()
        self.topLevel.title('Waste Transport Data Viewer')
        self.topLevel.state("zoomed")
        self.page_data = KpoRequests.KPO()
        self.all_items = []
        self.csv_file_name = csv_transmitter_file
        self.create_widgets()

    def generate_pdf(self):
        PdfCreator().gen_conf(self.tree,self.topLevel)

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

        self.load_data()

        self.tree.bind('<Double-1>', self.on_item_double_click)

        frame = tk.Frame(self.main_frame)
        frame.pack()

        self.details = ttk.Button(frame, text="Pokaż szczegóły", command=self.show_details)
        self.details.grid(row=0, column=1)

        self.remove = ttk.Button(frame, text="Wycofaj kartę", command=self.remove_card)
        self.remove.grid(row=0,column=2)

        self.generate_conf = ttk.Button(frame, text="Zmień status na Potwierdzona", command=self.gen_conf)
        self.generate_conf.grid(row=0, column=3)

        self.edit_con_card = ttk.Button(frame, text="Edytuj kartę Zatwierdzoną", command=self.edit_card)
        self.edit_con_card.grid(row=0, column=4)

        self.download_pdf = ttk.Button(frame, text="Wygeneruj pdf", command=self.generate_pdf)
        self.download_pdf.grid(row=0, column=5)

        self.topLevel.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.topLevel.mainloop()

    def edit_card(self):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection, 'values')
            selected_id = item[0]
            data = self.page_data.szczegoly_karty_zatwierdzona(selected_id, 0)
            item_full_table = []
            item_full_table.append(item)
            item_full_table.append(data)
            print("To jest cała tablica: " + str(item_full_table))
            if self.callback:
                self.callback(item_full_table)
                self.topLevel.after(100, self.topLevel.destroy)
                self.inter_window.destroy()
            else:
                print("Zwrot się nie powiódł.")
        else:
            pass

    def gen_conf(self):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection, 'values')
            selected_id = item[0]
            result = self.page_data.zmiana_statusu_karty_na_potwierdzenie_wygenerowane(selected_id, self.topLevel)
            if result:
                print("Błąd podczas zmiany statusu karty")
            else:
                self.update_csv_status(selected_id, 'Potwierdzenie wygenerowane')
                self.update_treeview_from_csv()
                print("Status karty zaktualizowany pomyślnie")

    def on_closing(self):
        self.topLevel.destroy()

    def load_data(self):
        if os.path.exists(self.csv_file_name):
            with open(self.csv_file_name, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['cardStatus'] == 'Zatwierdzona':
                        self.tree.insert("", tk.END, values=(
                            row['kpoId'], row['plannedTransportTime'].replace("T", " "), row['realTransportTime'].replace("T", " "), row['wasteCode'],
                            row['wasteCodeDescription'], row['vehicleRegNumber'], row['cardStatus'], row.get('cardNumber', 'Brak numeru karty'),
                            row['senderName'], row['receiverName']))
                        self.all_items.append(row)
        else:
            messagebox.showerror("Błąd", "Plik danych nie istnieje.", parent=self.topLevel)

    def remove_card(self):
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
                                                                                                      "1.0", tk.END)))
            confirm_button.grid(row=0, column=1)

        else:
            messagebox.showerror("Błąd", "Nie wybrano karty", parent=self.topLevel)


    def delete_card(self,card_id, remarks):
        if len(remarks) < 1:
            tk.messagebox.showerror("Błąd", "Wpisz powód wycofania karty.", parent=self.topLevel2)
        else:
            result = self.page_data.zmiana_statusu_na_wycofana(card_id,remarks, self.topLevel2)
            if result:
                print("Błąd")
            else:
                self.update_csv_status(card_id, 'Wycofana')
                self.update_treeview_from_csv()
            self.topLevel2.destroy()

    def on_item_double_click(self, event):
        self.show_details()
        print(self.all_items)

    def show_details(self):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection, 'values')
            selected_id = item[0]
            data = self.page_data.szczegoly_karty_zatwierdzona(selected_id,0)
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