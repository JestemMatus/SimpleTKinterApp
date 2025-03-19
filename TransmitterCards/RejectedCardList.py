import tkinter as tk
from tkinter import ttk, messagebox
import os
import KpoRequests
import csv
import CompanyLabel
from Globals import csv_transmitter_file, highlightbackground, highlightcolor
import WasteCopy
import SelectWasteWindow
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
        self.tree['columns'] = (
        'kpoId', 'plannedTransportTime', 'realTransportTime', 'wasteCode', 'wasteCodeDescription',
        'vehicleRegNumber', 'cardStatus','cardNumber','senderName', 'receiverName')

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

        self.correct_card_button = ttk.Button(frame, text="Dokonaj korekty karty", command=self.correct_card)
        self.correct_card_button.grid(row=0, column=2)

        self.download_pdf = ttk.Button(frame, text="Wygeneruj pdf", command=self.generate_pdf)
        self.download_pdf.grid(row=0, column=3)

        self.topLevel.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.topLevel.mainloop()


    def generate_pdf(self):
        PdfCreator().gen_conf(self.tree,self.topLevel)

    def correct_card(self):
        selection = self.tree.selection()
        if selection:
            self.selected_id = self.tree.item(selection, 'values')[0]
            waste_code = self.tree.item(selection, 'values')[3]
            self.toplevel2 = tk.Toplevel(self.topLevel)
            main_frame = ttk.Frame(self.toplevel2)
            main_frame.pack()

            info = KpoRequests.KPO().szczegoly_karty_odrzucona(self.selected_id,0)

            self.waste_code_id = info['wasteCodeId']
            waste_mass = info['wasteMass']
            waste_code_extended = info['wasteCodeExtended']
            waste_code_extended_description = info['wasteCodeExtendedDescription']
            hazardous_waste_reclassification = info['hazardousWasteReclassification']
            hazardous_waste_reclassification_description = info['hazardousWasteReclassificationDescription']

            frame1 = tk.Frame(main_frame, highlightcolor="#0063b1", highlightthickness=1, highlightbackground="#DCDCDC")
            waste_search_button = ttk.Button(frame1, text="Wyszukaj kod", command=self.open_waste_window)
            waste_search_button.grid()
            self.waste_code_entry = ttk.Entry(frame1)
            self.waste_code_entry.grid(padx=65, pady=(0,5))
            self.waste_code_entry.insert(0,waste_code)
            frame1.grid(row=0, column=0,pady=4, padx=10)

            frame2 = tk.Frame(main_frame, highlightcolor="#0063b1", highlightthickness=1, highlightbackground="#DCDCDC")
            mass_label = ttk.Label(frame2, text="Masa odpadu w tonach [Mg]:")
            mass_label.grid(pady=3)

            vcmd = (self.toplevel2.register(self.on_validate), '%P')

            self.mass_entry = ttk.Entry(frame2, validate='key', validatecommand=vcmd)
            self.mass_entry.grid(padx=65, pady=(0,5))
            self.mass_entry.insert(0, waste_mass)
            frame2.grid(row=0 , column=1,pady=4, padx=10)

            frame3 = tk.Frame(main_frame, highlightcolor="#0063b1", highlightthickness=1, highlightbackground="#DCDCDC")
            self.check_state = tk.BooleanVar(value=waste_code_extended)
            check_button = ttk.Checkbutton(frame3, text="Rozszerzony kod odpadu", variable=self.check_state,
                                           command=self.check_button_changed)
            check_button.grid()

            self.extended_waste_description = tk.Text(frame3, height=8, width=30)
            self.extended_waste_description.grid(padx=5, pady=(0,5))

            if self.check_state.get():
                self.extended_waste_description.configure(state="normal", background="white")
                self.extended_waste_description.insert("1.0", waste_code_extended_description)
            else:
                self.extended_waste_description.configure(state="disabled", background="#f0f0f0")
            frame3.grid(row=1, column=0, padx=10, pady=4)

            frame4 = tk.Frame(main_frame, highlightcolor="#0063b1", highlightthickness=1, highlightbackground="#DCDCDC")
            self.check_state2 = tk.BooleanVar(value=hazardous_waste_reclassification)
            check_button = ttk.Checkbutton(frame4, text="Reklasyfikacja jako odpad niebezpieczny",
                                           variable=self.check_state2, command=self.check_button_changed2)
            check_button.grid()

            self.hazardous_waste_reclassification_description = tk.Text(frame4, height=8, width=30)
            self.hazardous_waste_reclassification_description.grid(padx=5, pady=(0,5))

            if self.check_state2.get():
                self.hazardous_waste_reclassification_description.configure(state="normal", background="white")
                self.hazardous_waste_reclassification_description.insert("1.0", hazardous_waste_reclassification_description)
            else:
                self.hazardous_waste_reclassification_description.configure(state="disabled", background="#f0f0f0")
            frame4.grid(row=1, column=1, padx=10, pady=4)

            frame5 = tk.Frame(main_frame)
            frame5.grid(row=2, column=0, columnspan=2)

            back_button = ttk.Button(frame5, text="Anuluj", command=self.toplevel2.destroy)
            back_button.grid(row=0, column=0)

            apply_button = ttk.Button(frame5, text="Potwierdź", command=self.confirm_all)
            apply_button.grid(row=0, column=1)

            self.toplevel2.mainloop()

    def check_first(self):
        if self.check_state.get():
            text_content = self.extended_waste_description.get("1.0", tk.END).strip()
            if not text_content:
                tk.messagebox.showwarning("Ostrzeżenie", "Pole opisu poniżej rozszerzonego\nkodu odpadów nie może być puste.", parent=self.toplevel2)
                return False
            else:
                return True
        else:
            return True

    def check_second(self):
        if self.check_state2.get():
            text_content = self.hazardous_waste_reclassification_description.get("1.0", tk.END).strip()
            if not text_content:
                tk.messagebox.showwarning("Ostrzeżenie", "Pole opisu poniżej reklasyfikacji\nodpadu nie może być puste.", parent=self.toplevel2)
                return False
            else:
                return True
        else:
            return True

    def confirm_all(self):
        check_field1 = self.check_first()
        check_field2 = self.check_second()

        if check_field1==True and check_field2==True:
            mass_before = self.mass_entry.get()
            mass = self.replace_comma_with_dot(mass_before)
            if self.check_state.get():
                waste_code_extended = True
            else:
                waste_code_extended = False

            if self.check_state2.get():
                hazardous_waste_reclassification = True
            else:
                hazardous_waste_reclassification = False

            waste_code_extended_description = self.extended_waste_description.get("1.0",
                                                                                  tk.END).strip() if self.check_state.get() else None
            hazardous_waste_reclassification_description = self.hazardous_waste_reclassification_description.get("1.0",
                                                                                                                 tk.END).strip() if self.check_state2.get() else None

            data = {
                "KpoId": self.selected_id,
                "WasteCodeId": self.waste_code_id,
                "WasteMass": mass,
                "WasteCodeExtended": waste_code_extended,
                "WasteCodeExtendedDescription": waste_code_extended_description,
                "HazardousWasteReclassification": hazardous_waste_reclassification,
                "HazardousWasteReclassificationDescription": hazardous_waste_reclassification_description
            }

            result = KpoRequests.KPO().korekta_karty_odrzuconej(data, self.toplevel2)
            if result:
                print("Błąd podczas zmiany statusu karty")
            else:
                self.update_csv_status(self.selected_id, 'Potwierdzenie wygenerowane')
                self.update_treeview_from_csv()
                print("Status karty zaktualizowany pomyślnie")

            self.toplevel2.destroy()
        else:
            print("Błąd")

    @staticmethod
    def replace_comma_with_dot(input_string):
        return input_string.replace(',', '.')

    def my_callback(self, selected_code):
        self.waste_code_entry.delete(0,tk.END)
        self.waste_code_entry.insert(0, selected_code)
        self.waste_all = WasteCopy.WasteCode().search_code(selected_code)[0]
        self.waste_code_id = self.waste_all['wasteCodeId']

    def open_waste_window(self):
        SelectWasteWindow.WasteWindow(callback=self.my_callback).window()

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

    def check_button_changed2(self):
        if self.check_state2.get():
            self.hazardous_waste_reclassification_description.delete("1.0", tk.END)
            self.hazardous_waste_reclassification_description.configure(state="normal", background="white")
        else:
            self.hazardous_waste_reclassification_description.delete("1.0", tk.END)
            self.hazardous_waste_reclassification_description.configure(state="disabled", background="#f0f0f0")

    def check_button_changed(self):
        if self.check_state.get():
            self.extended_waste_description.delete("1.0", tk.END)
            self.extended_waste_description.configure(state="normal", background="white")
        else:
            self.extended_waste_description.delete("1.0", tk.END)
            self.extended_waste_description.configure(state="disabled", background="#f0f0f0")

    def on_closing(self):
        self.topLevel.destroy()

    def load_data(self):
        if os.path.exists(self.csv_file_name):
            with open(self.csv_file_name, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['cardStatus'] == 'Odrzucona':
                        self.tree.insert("", tk.END, values=(
                            row['kpoId'], row['plannedTransportTime'].replace('T', ' '), row['realTransportTime'].replace('T', ' '), row['wasteCode'],
                            row['wasteCodeDescription'], row['vehicleRegNumber'], row['cardStatus'],row['cardNumber'], row['senderName'],
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
            data = self.page_data.szczegoly_karty_odrzucona(selected_id, 0)
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
