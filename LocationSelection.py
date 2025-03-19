import tkinter as tk
from tkinter import ttk, messagebox
import ApiConnection

class Application():
    def __init__(self, callback=None):
        self.callback = callback
        self.topLevel = tk.Tk()
        self.topLevel.title('Paginated Data Viewer')
        self.topLevel.geometry('800x600')
        self.page_data = ApiConnection.Connection()
        self.create_widgets()

    def create_widgets(self):
        self.main_frame = tk.Frame(self.topLevel)
        self.main_frame.pack()

        self.label = tk.Label(self.main_frame, text="Wybierz miejsce prowadzenia działalności")
        self.label.pack()

        self.tree = ttk.Treeview(self.main_frame, show='headings', height=5)
        self.tree['columns'] = ('number', 'eupId', 'name', 'identificationNumber')

        self.tree.heading('number', text='#')
        self.tree.column('number', width=30, anchor=tk.CENTER)
        self.tree.heading('eupId', text='EupId')
        self.tree.column('eupId', width=240, anchor=tk.CENTER)
        self.tree.heading('name', text='Name')
        self.tree.column('name', width=220, anchor=tk.CENTER)
        self.tree.heading('identificationNumber', text='Identification Number')
        self.tree.column('identificationNumber', width=120, anchor=tk.CENTER)

        self.tree.pack(expand=True, fill=tk.BOTH)
        self.load_data()

        self.tree.bind('<Double-1>', self.on_item_double_click)

        frame = tk.Frame(self.main_frame)
        frame.pack()

        self.select = ttk.Button(frame, text="Wybierz", command=self.invoke_callback)
        self.select.grid(row=0, column=0)

        self.details = ttk.Button(frame, text="Szczegóły", command=self.show_details)
        self.details.grid(row=0, column=1)

        self.topLevel.mainloop()

    def on_item_double_click(self, event):
        self.invoke_callback()


    def load_data(self):
        self.page_number = 1
        hasNextPage = True

        while hasNextPage:
            page_data = self.page_data.show_access_attempt_with_auth(self.page_number)
            if page_data and 'items' in page_data:
                self.display_data(page_data['items'])
                hasNextPage = page_data.get('hasNextPage', False)
                self.page_number += 1
            else:
                print(f"Nie udało się załadować danych dla strony {self.page_number}.")
                hasNextPage = False

    def display_data(self, items):

        for item in items:
            self.tree.insert('', 'end', values=(self.page_number,item['eupId'], item['name'],
                                                item['identificationNumber']))

    def show_details(self):
        selection = self.tree.selection()
        if selection:
            selected_id = self.tree.item(selection, 'values')[0]
            info = self.page_data.show_access_attempt_with_auth(selected_id)
            tk.messagebox.showinfo("Info",info)
        else:
            pass

    def invoke_callback(self):
        selection = self.tree.selection()
        if selection:
            selected_item = self.tree.item(selection, 'values')
            selected_id = self.tree.item(selection, 'values')[0]
            ApiConnection.GetToken(selected_id).read_access_token_from_csv()
            if self.callback:
                self.callback(selected_item)
                self.topLevel.after(100, self.topLevel.destroy)
            else:
                print("Zwrot się nie powiódł.")
        else:
            pass

if __name__ == "__main__":
    app = Application()
    app.create_widgets()
