import tkinter as tk
from tkinter import ttk
import csv
import os

class CompanyFrame:
    def __init__(self, container, row, column, root, col_width):
        self.container = container
        self.row = row
        self.column = column
        self.root = root
        self.col_width = col_width
        self.access_data_csv_path = 'temp/Access_data.csv'

    def refresh_data(self):

        for i in self.tree.get_children():
            self.tree.delete(i)

        data_list = self.read_data_from_csv(self.access_data_csv_path)
        selected_columns = self.tree['columns']

        for item in data_list:
            values = [item.get(col, 'Brak') for col in selected_columns]
            self.tree.insert("", "end", values=values)

    @staticmethod
    def read_data_from_csv(csv_file):
        data_list = []
        default_value = 'Brak'

        if not os.path.exists(csv_file):
            print("Plik CSV nie istnieje.")
            return [{'name': default_value, 'identificationNumber': default_value, 'province': default_value,
                     'district': default_value, 'commune': default_value, 'locality': default_value,
                     'street': default_value, 'buildingNumber': default_value, 'localNumber': default_value}]

        with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:

                if not row:
                    data_list.append({col: default_value for col in reader.fieldnames})
                else:
                    data_list.append({col: (row[col] if row[col] else default_value) for col in reader.fieldnames})

        if not data_list:
            data_list.append({col: default_value for col in reader.fieldnames})

        return data_list


    def main_frame(self):
        data_list = self.read_data_from_csv(self.access_data_csv_path)

        selected_columns = ['name', 'identificationNumber', 'province', 'district', 'commune', 'locality', 'street', 'buildingNumber', 'localNumber']

        self.tree = ttk.Treeview(self.container, columns=selected_columns, show="headings", height=1)

        new_headings = {
            'name': 'Nazwa',
            'identificationNumber': 'Numer Identyfikacyjny',
            'province': 'Województwo',
            'district': 'Powiat',
            'commune': 'Gmina',
            'locality': 'Miejscowość',
            'street': 'Ulica',
            'buildingNumber': 'Numer Budynku',
            'localNumber': 'Numer Lokalu',
        }

        for col in selected_columns:
            self.tree.heading(col, text=new_headings.get(col, col))
            self.tree.column(col, width= self.col_width)

        self.tree.grid(row=0, column=0, columnspan=len(selected_columns))

        for item in data_list:
            values = [item[col] for col in selected_columns]
            self.tree.insert("", "end", values=values)

if __name__ == "__main__":
    root = tk.Tk()
    container = tk.Frame(root)
    container.grid()
    test = CompanyFrame(container, 0, 0, root,122)
    test.main_frame()

    refresh_button = tk.Button(root, text="Odśwież", command= test.refresh_data)
    refresh_button.grid()

    root.mainloop()
