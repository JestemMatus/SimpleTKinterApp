import tkinter as tk
from tkinter import ttk
import Waste

class WasteProcessWindow:
    def __init__(self, callback=None):
        self.waste = Waste.WasteProccess()
        self.list_of_codes = self.waste.process_list()
        self.callback = callback

    def window(self):
        self.window = tk.Toplevel()

        self.frame = tk.Frame(self.window)
        self.frame.pack()

        self.select_button = ttk.Button(self.frame, text="Wybierz", command=self.select_item)
        self.select_button.grid(row=0, column=0)

        self.back_button = ttk.Button(self.frame, text="Cofnij", command=self.back, state='disabled')
        self.back_button.grid(row=0, column=1)

        self.tree = ttk.Treeview(self.window, columns=("id", "name", "codename"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("codename", text="Codename")
        self.tree.column("id", width=60)
        self.tree.column("name", width=200)
        self.tree.column("codename", width=200)
        self.tree.bind("<Double-1>", self.on_item_double_click)

        self.fill_treeview()

        scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        self.window.mainloop()

    def fill_treeview(self, parent_id=None):
        self.tree.delete(*self.tree.get_children())
        if parent_id is None:
            filtered_data = [item for item in self.list_of_codes if item['parentId'] is None]
            self.select_button['state'] = 'disabled'
            self.back_button['state'] = 'disabled'
        else:
            filtered_data = [item for item in self.list_of_codes if item['parentId'] == parent_id]
            self.select_button['state'] = 'normal'
            self.back_button['state'] = 'normal'

        for item in filtered_data:
            self.tree.insert('', 'end', values=(item["wasteProcessId"], item["name"], item["codeName"]))

    def back(self):

        self.fill_treeview()

    def select_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            selected_id = self.tree.item(selected_item, 'values')
            if self.callback:
                self.callback(selected_id)
            self.window.destroy()

    def on_item_double_click(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            selected_id = self.tree.item(selected_item, 'values')[0]
            if self.has_children(selected_id):
                self.fill_treeview(int(selected_id))
            else:
                self.select_item()

    def has_children(self, selected_id):
        return any(item['parentId'] == int(selected_id) for item in self.list_of_codes)

    def get_current_level(self, selected_id):
        for item in self.list_of_codes:
            if item['wasteProcessId'] == int(selected_id):
                return item.get('level')
        return None

