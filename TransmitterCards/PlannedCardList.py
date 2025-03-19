import tkinter as tk
from tkinter import ttk, messagebox
import os
import KpoRequests
from Globals import csv_transmitter_file, highlightbackground, highlightcolor
import csv
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
                                'vehicleRegNumber', 'cardStatus', 'senderName', 'receiverName')

        self.tree.heading('kpoId', text='Id_karty')
        self.tree.column('kpoId', width=0, minwidth=0, stretch=tk.NO)
        self.tree.heading('plannedTransportTime', text='Planowany czas transportu', anchor="center")
        self.tree.column('plannedTransportTime', width=120, anchor="center")
        self.tree.heading('realTransportTime', text='Rzeczywisty czas transportu', anchor="center")
        self.tree.column('realTransportTime', width=120, anchor="center")
        self.tree.heading('wasteCode', text='Kod', anchor="center")
        self.tree.column('wasteCode', width=60, anchor="center")
        self.tree.heading('wasteCodeDescription', text='Opis kodu odpadów', anchor="center")
        self.tree.column('wasteCodeDescription', width=200, anchor="center")
        self.tree.heading('vehicleRegNumber', text='Numer rejestracyjny pojazdu', anchor="center")
        self.tree.column('vehicleRegNumber', width=80, anchor="center")
        self.tree.heading('cardStatus', text='Status karty', anchor="center")
        self.tree.column('cardStatus', width=100, anchor="center")
        self.tree.heading('senderName', text='Nazwa nadawcy', anchor="center")
        self.tree.column('senderName', width=275, anchor="center")
        self.tree.heading('receiverName', text='Nazwa odbiorcy', anchor="center")
        self.tree.column('receiverName', width=275, anchor="center")


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

        self.edit = ttk.Button(frame, text="Edytuj kartę", command=self.edit_card)
        self.edit.grid(row=0, column=2)

        self.delete = ttk.Button(frame, text="Usuń kartę ze statusem planowana", command=self.delete_card)
        self.delete.grid(row=0, column=3)

        self.confirm = ttk.Button(frame, text="Zatwierdź kartę", command=self.confrim_card)
        self.confirm.grid(row=0,column=4)

        self.topLevel.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.topLevel.mainloop()

    @staticmethod
    def update_card_number_in_csv(kpo_id, new_card_number, csv_file_name):
        folder, filename = os.path.split(csv_file_name)
        name, ext = os.path.splitext(filename)

        temp_file_name = os.path.join(folder, 'temp_' + name + ext)
        print(temp_file_name)

        fieldnames = ['kpoId', 'plannedTransportTime', 'realTransportTime', 'wasteCode', 'wasteCodeDescription',
                      'vehicleRegNumber', 'cardStatus', 'cardNumber', 'senderName', 'receiverName']

        updated = False
        with open(csv_file_name, mode='r', newline='', encoding='utf-8') as csvfile, \
                open(temp_file_name, mode='w', newline='', encoding='utf-8') as temp_file:
            reader = csv.DictReader(csvfile, fieldnames=fieldnames)
            writer = csv.DictWriter(temp_file, fieldnames=fieldnames)

            writer.writeheader()

            for row in reader:
                if row['kpoId'] == kpo_id:
                    row['cardNumber'] = new_card_number
                    updated = True
                writer.writerow(row)

        if updated:
            os.remove(csv_file_name)
            os.rename(temp_file_name, csv_file_name)
        else:
            os.remove(temp_file_name)

        return updated


    def confrim_card(self):
        selection = self.tree.selection()
        if selection:
            card_id = self.tree.item(selection, 'values')[0]
            result = self.page_data.zmiana_statusu_karty_z_planowanej_na_zatwierdzona(card_id, self.topLevel)
            if result:
                print("Błąd podczas zmiany statusu karty")
            else:
                self.update_csv_status(card_id, 'Zatwierdzona')
                data = self.page_data.szczegoly_karty_zatwierdzona(card_id, 0)
                cardNumber = data['cardNumber']
                self.update_card_number_in_csv(card_id,cardNumber,self.csv_file_name)
                self.update_treeview_from_csv()

    def on_closing(self):
        self.topLevel.destroy()

    def delete_card(self):
        selection = self.tree.selection()
        if selection:
            card_id = self.tree.item(selection, 'values')[0]
            result = self.page_data.usuwanie_karty_ze_statusem_planowana(card_id,self.topLevel)
            if result:
                print("Błąd")
            else:
                self.update_csv_after_deletion(card_id)
                self.update_treeview_from_csv()

    def edit_card(self):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection, 'values')
            selected_id = item[0]
            data = self.page_data.szczegoly_karty_planowana(selected_id, 0)
            item_full_table = []
            item_full_table.append(item)
            item_full_table.append(data)
            print("To jest cała tablica: "+str(item_full_table))
            if self.callback:
                self.callback(item_full_table)
                self.topLevel.after(100, self.topLevel.destroy)
                self.inter_window.destroy()
            else:
                print("Zwrot się nie powiódł.")
        else:
            pass

    def load_data(self):
        self.all_items.clear()
        if os.path.exists(self.csv_file_name):
            with open(self.csv_file_name, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['cardStatus'] == 'Planowana':
                        self.tree.insert("", tk.END, values=(
                            row['kpoId'], row['plannedTransportTime'].replace("T", " "), row['realTransportTime'].replace("T", " "), row['wasteCode'],
                            row['wasteCodeDescription'], row['vehicleRegNumber'], row['cardStatus'], row['senderName'],
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
            data = self.page_data.szczegoly_karty_planowana(selected_id,0)
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

if __name__ == '__main__':
    root = tk.Tk()
    CardsListApplication(root, None).create_widgets()
    root.mainloop()

