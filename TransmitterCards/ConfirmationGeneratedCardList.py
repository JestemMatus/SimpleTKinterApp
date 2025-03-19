import tkinter as tk
from tkinter import ttk, messagebox
import os
import KpoRequests
import csv
from Globals import csv_transmitter_file, highlightcolor, highlightbackground
from PdfCreator import PdfCreator
import CompanyLabel

"ApprovedCardList"

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
        self.tree['columns'] = (
        'kpoId', 'plannedTransportTime', 'realTransportTime', 'wasteCode', 'wasteCodeDescription',
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

        reject_button = ttk.Button(frame, text="Odrzuć kartę", command=self.remove_card)
        reject_button.grid(row=0, column=2)

        self.generate_conf = ttk.Button(frame, text="Wygeneruj potwierdzenie PDF", command=self.generate_pdf)
        self.generate_conf.grid(row=0, column=3)

        self.generate_card = ttk.Button(frame, text="Wygeneruj PDF Karty", command=self.gen_conf)
        self.generate_card.grid(row=0, column=4)

        self.receiverconfirmation = ttk.Button(frame, text="Zmień status na Potwierdzenie przejęcia", command=self.receiver_conf)
        self.receiverconfirmation.grid(row=0, column=5)

        self.topLevel.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.topLevel.mainloop()

    def generate_pdf(self):
        PdfCreator().gen_conf_card(self.tree,self.topLevel)

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
        result = KpoRequests.KPO().Zmiana_statusu_karty_z_wygenerowane_potwierdzenie_na_potwierdzenie_przyjecia(kpo_id,mass,remarks, self.topLevel)
        if result:
            print("Błąd podczas zmiany statusu karty")
        else:
            self.update_csv_status(kpo_id, 'Potwierdzenie przejęcia')
            self.update_treeview_from_csv()
        self.topLevel2.destroy()

    def gen_conf(self):
        PdfCreator.gen_conf(self.tree,self.topLevel)

    def on_closing(self):
        self.topLevel.destroy()

    def load_data(self):
        if os.path.exists(self.csv_file_name):
            with open(self.csv_file_name, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['cardStatus'] == 'Potwierdzenie wygenerowane':
                        self.tree.insert("", tk.END, values=(
                            row['kpoId'], row['plannedTransportTime'].replace('T', ' '), row['realTransportTime'].replace('T', ' '), row['wasteCode'],
                            row['wasteCodeDescription'], row['vehicleRegNumber'], row['cardStatus'], row['cardNumber'],row['senderName'],
                            row['receiverName']))
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

    def delete_card(self, card_id, remarks):
        if len(remarks) < 1:
            tk.messagebox.showerror("Błąd", "Wpisz powód odrzucenia karty.", parent=self.topLevel2)
        else:
            result = self.page_data.zmiana_statusu_na_odrzucona(card_id,remarks, self.topLevel2)
            if result:
                print("Błąd")
            else:
                self.update_csv_status(card_id, 'Odrzucona')
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
            data = self.page_data.szczegoly_karty_wygenerowane_potwierdzenie(selected_id, 0)
            print(data)
            details_message = "Szczegóły transportu:\n\n" + "\n".join(
                f"{k}: {v}" for k, v in zip(self.tree['columns'], item))
            messagebox.showinfo("Szczegóły", details_message + str(data), parent=self.topLevel)

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
