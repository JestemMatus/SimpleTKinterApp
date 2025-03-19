import tkinter as tk
from tkinter import ttk
import KpoRequests
import threading

class Receiver_window:
    def __init__(self, callback=None):
        self.company_list = KpoRequests.Search()
        self.data = []
        self.original_data = []
        self.selected_company_id = None
        self.view_history = []
        self.entry_histoyy = []
        self.callback = callback

    def window(self):
        self.column_visibility = {
            'CompanyID': True,
            'registrationNumber': True,
            'name': True,
            'nipEu': True,
            'nip': True,
            'pesel': True,
            'country': True,
            'address': True,
            'buildingNumber': True,
            'localNumber': True,
            'postalCode': True,
            'teryt': True
        }

        self.window = tk.Toplevel()

        self.tk_entry = ttk.Entry(self.window)
        self.tk_entry.insert(0, "Wyszukaj pod dowolnym parametrze")
        self.tk_entry.bind("<FocusIn>", self.on_entry_click)
        self.tk_entry.bind("<KeyRelease>", self.on_text_change)
        self.tk_entry.pack(pady=10)

        self.back_button = ttk.Button(self.window, text="Powrót", command=self.back, state="disabled")
        self.back_button.pack()

        self.tree_company = ttk.Treeview(self.window, columns=(
            'CompanyID', 'registrationNumber', 'name', 'nipEu', 'nip', 'pesel', 'country', 'address', 'buildingNumber',
            'localNumber', 'postalCode', 'teryt'), show='headings')

        for col in self.tree_company['columns']:
            self.tree_company.heading(col, text=col)
            self.tree_company.column(col, width=80, stretch=True)

        self.fill_treeview()

        self.select_button = ttk.Button(self.window, text="Wybierz", command=self.select_action, state="disabled")
        self.select_button.pack()

        self.tree_company.pack()
        self.tree_company.bind("<Double-1>", self.on_item_double_click)
        self.level = 1



        frame = tk.Frame(self.window)
        frame.pack(side="bottom")

        self.visibility_buttons = {col: ttk.Checkbutton(
            frame, text=col, command=lambda col=col: self.toggle_column_visibility(col))
            for col in self.tree_company['columns']}

        for col, btn in self.visibility_buttons.items():
            btn.pack(side="left")
        self.update_column_visibility()

        self.window.mainloop()


    def select_action(self):
        selected_item = self.tree_company.selection()
        if selected_item:
            self.selected_eup_data = self.tree_company.item(selected_item, 'values')[0]


            self.finish(self.selected_eup_data)


    def on_second_item_double_click(self, event):
        selected_item = self.tree_company.selection()
        if selected_item:
            self.selected_eup_data = self.tree_company.item(selected_item, 'values')
            self.finish(self.selected_eup_data)

    def finish(self, selected_company_eup):
        print("KONIEC, wybrany eupid to:" +str(selected_company_eup))
        combined_data = (selected_company_eup, self.first_treeview_table)

        if self.callback:
            self.callback(combined_data)
        self.window.destroy()

    def update_column_visibility(self):
        for col in self.column_visibility:
            if self.column_visibility[col]:
                self.tree_company.column(col, width=80)
            else:
                self.tree_company.column(col, width=0)

    def recreate_treeview(self, columns):
        if self.tree_company is not None:
            self.tree_company.destroy()

        self.tree_company = ttk.Treeview(self.window, columns=columns, show='headings')
        for col in columns:
            self.tree_company.heading(col, text=col)
            self.tree_company.column(col, width=80)
        self.tree_company.pack(fill='both', expand=True)
        self.tree_company.bind("<Double-1>", self.on_item_double_click)

        for col in self.column_visibility:
            self.column_visibility[col] = True
            self.visibility_buttons[col].state(['!selected'])
        self.select_button['state'] = "disabled"

    def toggle_column_visibility(self, column_id):
        if self.column_visibility[column_id]:

            self.tree_company.column(column_id, width=0)
            self.tree_company.heading(column_id,)
        else:

            self.tree_company.column(column_id, width=80)
        self.column_visibility[column_id] = not self.column_visibility[column_id]

    def on_item_double_click(self, event):
        selected_item = self.tree_company.selection()
        if selected_item:
            self.first_treeview_table = self.tree_company.item(selected_item, 'values')
            self.selected_company_id = self.tree_company.item(selected_item, 'values')[0]
            self.view_history.append(("general", self.selected_company_id))
            self.update_treeview_with_details(self.selected_company_id)
            self.back_button['state'] = "normal"

    def back(self):
        if self.view_history:
            view_type, company_id_to_select = self.view_history.pop()
            if view_type == "general":
                self.recreate_general_treeview()
                last_search = self.entry_histoyy[-1] if self.entry_histoyy else ''
                self.tk_entry.delete(0, tk.END)
                self.tk_entry.insert(0, last_search)
                self.query_database(last_search, company_id_to_select=company_id_to_select)
            self.back_button['state'] = "normal" if self.view_history else "disabled"

    def recreate_general_treeview(self):
        if self.tree_company is not None:
            self.tree_company.destroy()

        self.tree_company = ttk.Treeview(self.window, columns=(
            'CompanyID', 'registrationNumber', 'name', 'nipEu', 'nip', 'pesel', 'country', 'address', 'buildingNumber',
            'localNumber', 'postalCode', 'teryt'), show='headings')

        for col in self.tree_company['columns']:
            self.tree_company.heading(col, text=col)
            self.tree_company.column(col, width=80)

        self.tree_company.pack(fill='both', expand=True)
        self.tree_company.bind("<Double-1>", self.on_item_double_click)
        self.select_button['state'] = "disabled"

    def update_treeview_with_columns(self, columns):

        self.tree_company['columns'] = columns
        for col in columns:
            self.tree_company.column(col, width=80)
            self.tree_company.heading(col, text=col)
        self.update_treeview(self.data)

    def update_treeview_with_details(self, selected_company_id):
        newdata = self.company_list.Zwroc10rekorwowzdanymimiejscprowadzeniadzialanosci(selected_company_id)
        self.recreate_treeview(
            ['eupId', 'companyId', 'registrationNumber', 'name', 'address', 'buildingNumber', 'localNumber',
             'postalCode', 'teryt'])
        for item in newdata:
            self.tree_company.insert('', 'end', values=(
                item.get('eupId', ''),
                item.get('companyId', ''),
                item.get('registrationNumber', ''),
                item.get('name', ''),
                item.get('address', ''),
                item.get('buildingNumber', ''),
                item.get('localNumber', ''),
                item.get('postalCode', ''),
                item.get('teryt', '')
            ))
        self.tree_company.bind("<Double-1>", self.on_second_item_double_click)
        self.select_button['state'] = "normal"

    def get_details(self):
        print("tu działa")

    def fill_treeview(self):
        self.data = self.company_list.ZwracaListeRekordowZgodniezwartosciazapytania('')
        self.update_treeview(self.data)
        self.select_row_based_on_history()

    def select_row_based_on_history(self):
        print("self.history view: "+str(self.view_history))
        if self.view_history:
            _, last_selected_company_id = self.view_history[-1]
            for child in self.tree_company.get_children():
                print("tu powinno być id"+str(self.tree_company.item(child,'values')[0]))
                if self.tree_company.item(child, 'values')[0] == last_selected_company_id:
                    self.tree_company.selection_set(child)
                    break

    def on_entry_click(self, event):
        if self.tk_entry.get() == "Wyszukaj pod dowolnym parametrze":
            self.tk_entry.delete(0, tk.END)

    def on_text_change(self, event):
        search_text = self.tk_entry.get()
        if search_text != "Wyszukaj pod dowolnym parametrze":

            threading.Thread(target=self.query_database, args=(search_text,), daemon=True).start()
            self.entry_histoyy.append(search_text)

    def query_database(self, search_text, company_id_to_select=None):
        filtered_data = self.company_list.ZwracaListeRekordowZgodniezwartosciazapytania(search_text)
        self.tree_company.after(0, lambda: self.update_treeview(filtered_data, company_id_to_select))

    def update_treeview(self, data, company_id_to_select=None):
        if self.tree_company.winfo_exists():
            self.tree_company.delete(*self.tree_company.get_children())
        for item in data:
            inserted = self.tree_company.insert('', 'end', values=(
                item.get('companyId', ''),
                item.get('registrationNumber', ''),
                item.get('name', ''),
                item.get('nipEu', ''),
                item.get('nip', ''),
                item.get('pesel', ''),
                item.get('country', ''),
                item.get('address', ''),
                item.get('buildingNumber', ''),
                item.get('localNumber', ''),
                item.get('postalCode', ''),
                item.get('teryt', '')
            ))
            if company_id_to_select and item.get('companyId', '') == company_id_to_select:
                self.tree_company.selection_set(inserted)

class Transporter_window:
    def __init__(self, callback=None):
        self.company_list = KpoRequests.Search()
        self.data = []  # Dane
        self.callback = callback

    def window(self):
        self.window = tk.Toplevel()

        self.tk_entry = ttk.Entry(self.window)
        self.tk_entry.insert(0, "Wyszukaj pod dowolnym parametrze")
        self.tk_entry.bind("<FocusIn>", self.on_entry_click)
        self.tk_entry.bind("<KeyRelease>", self.on_text_change)
        self.tk_entry.pack(pady=10)

        self.tree_company = ttk.Treeview(self.window, columns=(
            'CompanyId', 'registrationNumber', 'name', 'nipEu', 'nip', 'pesel', 'country', 'address',
            'buildingNumber',
            'localNumber', 'postalCode', 'teryt'), show='headings')

        for col in self.tree_company['columns']:
            self.tree_company.heading(col, text=col)
            self.tree_company.column(col, width=80, stretch=True)

        self.fill_treeview()

        self.select_button = ttk.Button(self.window, text="Wybierz", command=self.select_action)
        self.select_button.pack()

        self.tree_company.pack()
        self.tree_company.bind("<Double-1>", self.on_item_double_click)

        frame = tk.Frame(self.window)
        frame.pack(side="bottom")

        self.visibility_buttons = {col: ttk.Checkbutton(
            frame, text=col, command=lambda col=col: self.toggle_column_visibility(col))
            for col in self.tree_company['columns']}

        for col, btn in self.visibility_buttons.items():
            btn.pack(side="left")

        self.window.mainloop()

    def fill_treeview(self):
        self.data = self.company_list.ZwracaListeRekordowZgodniezwartosciazapytania('')
        self.update_treeview(self.data)

    def update_treeview(self, data):
        self.tree_company.delete(*self.tree_company.get_children())
        for item in data:
            print(item)
            self.tree_company.insert('', 'end', values=(
                item.get('companyId', ''),
                item.get('registrationNumber', ''),
                item.get('name', ''),
                item.get('nipEu', ''),
                item.get('nip', ''),
                item.get('pesel', ''),
                item.get('country', ''),
                item.get('address', ''),
                item.get('buildingNumber', ''),
                item.get('localNumber', ''),
                item.get('postalCode', ''),
                item.get('teryt', '')
            ))

    def toggle_column_visibility(self, column_id):
        current_width = self.tree_company.column(column_id, option="width")
        if current_width > 0:
            self.tree_company.column(column_id, width=0)
        else:
            self.tree_company.column(column_id, width=80)

    def on_entry_click(self, event):
        if self.tk_entry.get() == "Wyszukaj pod dowolnym parametrze":
            self.tk_entry.delete(0, tk.END)

    def on_text_change(self, event):
        search_text = self.tk_entry.get()
        if search_text != "Wyszukaj pod dowolnym parametrze":
            threading.Thread(target=self.query_database, args=(search_text,), daemon=True).start()

    def query_database(self, search_text):
        filtered_data = self.company_list.ZwracaListeRekordowZgodniezwartosciazapytania(search_text)
        self.tree_company.after(0, lambda: self.update_treeview(filtered_data))

    def on_item_double_click(self, event):
        selected_item = self.tree_company.selection()
        if selected_item:
            self.select_button['state'] = "normal"
            self.selected_company = self.tree_company.item(selected_item, 'values')
            self.finish(self.selected_company)

    def select_action(self):
        selected_item = self.tree_company.selection()
        if selected_item:
            selected_company = self.tree_company.item(selected_item, 'values')
            self.finish(selected_company)

    def finish(self, selected_company):
        print("Wybrano firmę o ID:", selected_company)
        if self.callback:
            self.callback(selected_company)
        self.window.destroy()



class SelectTeryt:
    def __init__(self, callback=None):
        self.teryt_list = KpoRequests.Search()
        self.data = []  # Dane
        self.callback = callback

    def window(self):
        self.window = tk.Toplevel()

        self.tk_entry = ttk.Entry(self.window)
        self.tk_entry.insert(0, "Wyszukaj pod dowolnym parametrze")
        self.tk_entry.bind("<FocusIn>", self.on_entry_click)
        self.tk_entry.bind("<KeyRelease>", self.on_text_change)
        self.tk_entry.pack(pady=10)

        self.tree_company = ttk.Treeview(self.window, columns=(
            'Numer teryt', 'Teryt', 'Rodzaj gminy', 'Gmina', 'Powiat', 'Województwo'), show='headings')

        column_widths = {
            'Numer teryt': 80,
            'Teryt': 300,
            'Rodzaj gminy': 120,
            'Gmina': 120,
            'Powiat': 120,
            'Województwo': 120
        }

        for col in self.tree_company['columns']:
            self.tree_company.heading(col, text=col)
            self.tree_company.column(col, width=column_widths.get(col, 100), stretch=True)

        self.fill_treeview()

        self.select_button = ttk.Button(self.window, text="Wybierz", command=self.select_action)
        self.select_button.pack()

        self.tree_company.pack()
        self.tree_company.bind("<Double-1>", self.on_item_double_click)

        frame = tk.Frame(self.window)
        frame.pack(side="bottom")

        self.visibility_buttons = {col: ttk.Checkbutton(
            frame, text=col, command=lambda col=col: self.toggle_column_visibility(col))
            for col in self.tree_company['columns']}

        for col, btn in self.visibility_buttons.items():
            btn.pack(side="left")

        self.window.mainloop()

    def fill_treeview(self):
        self.data = self.teryt_list.ZwracaListeGmin('')
        self.update_treeview(self.data)

    def update_treeview(self, data):
        self.tree_company.delete(*self.tree_company.get_children())
        for item in data:
            self.tree_company.insert('', 'end', values=(
                item.get('PK', ''),
                item.get('fulltext', ''),
                item.get('rodzaj_gminy', ''),
                item.get('gmina', ''),
                item.get('powiat', ''),
                item.get('wojewodztwo', ''),
            ))

    def toggle_column_visibility(self, column_id):
        current_width = self.tree_company.column(column_id, option="width")
        if current_width > 0:
            self.tree_company.column(column_id, width=0)
        else:
            self.tree_company.column(column_id, width=80)

    def on_entry_click(self, event):
        if self.tk_entry.get() == "Wyszukaj pod dowolnym parametrze":
            self.tk_entry.delete(0, tk.END)

    def on_text_change(self, event):
        search_text = self.tk_entry.get()
        if search_text != "Wyszukaj pod dowolnym parametrze":
            threading.Thread(target=self.query_database, args=(search_text,), daemon=True).start()

    def query_database(self, search_text):
        filtered_data = self.teryt_list.ZwracaListeGmin(search_text)
        self.tree_company.after(0, lambda: self.update_treeview(filtered_data))

    def on_item_double_click(self, event):
        selected_item = self.tree_company.selection()
        if selected_item:
            self.select_button['state'] = "normal"
            self.selected_company = self.tree_company.item(selected_item, 'values')
            self.finish(self.selected_company)

    def select_action(self):
        selected_item = self.tree_company.selection()
        if selected_item:
            selected_company = self.tree_company.item(selected_item, 'values')
            self.finish(selected_company)

    def finish(self, selected_company):
        print("Wybrano teryt o ID:", selected_company)
        if self.callback:
            self.callback(selected_company)
        self.window.destroy()
