import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import Waste

class WasteWindow:
    def __init__(self, callback=None):
        self.view_history = []
        self.select_button = None
        self.waste = Waste.WasteCode()
        self.list_of_codes = self.waste.return_data()
        self.callback = callback


    def window(self):
        self.window = tk.Toplevel()
        divided_levels = self.divide_data_by_level(self.list_of_codes)

        self.tree = ttk.Treeview(self.window, columns=("code", "description"), show="headings")
        self.tree.heading("code", text="Code")
        self.tree.heading("description", text="Description")
        self.tree.column("code", width=60)
        self.tree.column("description", width=440)
        self.tree.bind("<Double-1>", self.on_item_double_click)

        self.frame = tk.Frame(self.window)
        self.frame.pack(side="top")

        self.back_button = ttk.Button(self.frame, text="Cofnij", command=self.back)
        self.back_button.grid(row=0, column=0)

        self.details_button = ttk.Button(self.frame, text="Szczegóły", command=self.details)
        self.details_button.grid(row=0, column=1)

        self.select_button = ttk.Button(self.frame, text="Wybierz", command=self.select, state="disabled")
        self.select_button.grid(row=0, column=2)

        scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        self.fill_treeview(divided_levels.get(1, []), level=1)
        self.window.mainloop()

    def fill_treeview(self, data, level):
        self.view_history.append((data, level))
        self.tree.delete(*self.tree.get_children())
        for item in data:
            self.tree.insert('', 'end', values=(item["code"], item["description"]))

        if level == 3:
            self.select_button['state'] = "normal"
            self.details_button['state'] = "normal"
        else:
            self.select_button['state'] = "disabled"
            self.details_button['state'] = "disabled"

    def on_item_double_click(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            selected_code = self.tree.item(selected_item, 'values')[0]
            current_level = self.view_history[-1][1]
            next_level = current_level + 1

            if next_level <= 3:
                filtered_data = [item for item in self.list_of_codes if
                                 item['level'] == next_level and item['code'].startswith(selected_code)]
                self.fill_treeview(filtered_data, level=next_level)
            elif current_level == 3:
                self.select()

    def select(self):
        selected_item = self.tree.selection()
        if selected_item:
            code = self.tree.item(selected_item, 'values')[0]
            if self.callback:
                self.callback(code)
            self.window.destroy()

    def details(self):
        selected_item = self.tree.selection()
        if selected_item:
            selected_code = self.tree.item(selected_item, 'values')[0]
            data = self.waste.search_code(selected_code)
            messagebox.showinfo("Szczegóły","Szczegóły: "+str(data))

    def back(self):
        if len(self.view_history) > 1:
            self.view_history.pop()
            previous_view = self.view_history.pop()
            self.fill_treeview(*previous_view)

    @staticmethod
    def divide_data_by_level(data):
        divided_data = {}
        for item in data:
            level = item['level']
            if level not in divided_data:
                divided_data[level] = []
            divided_data[level].append(item)
        return divided_data
