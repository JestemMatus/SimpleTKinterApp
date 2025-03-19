import tkinter as tk
from tkinter import ttk
import mysql.connector
from Globals import db_config
from tkinter import messagebox
from datetime import datetime

class DatabaseApp:
    def __init__(self, creator, callback=None):
        self.creator = creator
        self.callback = callback
        self.config_data = db_config
        self.host = db_config['host']
        self.user = db_config['user']
        self.password = db_config['password']
        self.database = db_config['database']
        self.create_toplevel()

    def create_toplevel(self):
        self.toplevel = tk.Toplevel()
        self.toplevel.title("Dane z bazy")

        frame = tk.Frame(self.toplevel)
        frame.pack()

        button = ttk.Button(frame, text="Importuj", command=self.getelements)
        button.grid(row=0, column=0)

        button_details = ttk.Button(frame, text="Szczegóły", command=self.on_item_double_click_event)
        button_details.grid(row=0, column=1)

        self.copy_button = ttk.Button(frame, text="Kopiuj wiersz", command=self.copy_selected)
        self.copy_button.grid(row=0, column=2)

        self.delete_from_history = ttk.Button(frame, text="Usuń z hisotrii", command=self.delete_item)
        self.delete_from_history.grid(row=0, column=3)

        column_widths = {
            "#": 30,
            "id": 0,
            "odbiorca": 150,
            "przewoźnik": 150,
            "kod odpadu": 80,
            "proces_odpadu": 50,
            "numer_rejestracyjny": 100,
            "masa_odpadu": 80,
            "planowany_czas_transportu": 150,
            "numer_certyfikatu": 100,
            "Dodatkowe informacje": 200
        }

        columns = list(column_widths.keys())

        self.tree = ttk.Treeview(self.toplevel, columns=columns, show="headings")
        for col in columns:
            if col == "id":
                self.tree.heading(col, text=col)
                self.tree.column(col, width=0, stretch=tk.NO)
            else:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=column_widths[col], anchor="center")

        self.tree.pack(expand=True, fill="both")

        self.load_data_from_db()

        self.tree.bind("<Double-1>", self.getelements)



        self.toplevel.mainloop()

    def on_item_double_click_event(self):
        event = None
        self.on_item_double_click(event)

    def copy_selected(self):
        selected_item = self.tree.selection()[0]
        self.selected_row_data = self.tree.item(selected_item, 'values')

        print("Skopiowano:", self.selected_row_data)

    def load_data_from_db(self):
        connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password,
                                             database=self.database)
        cursor = connection.cursor()

        cursor.execute("SHOW COLUMNS FROM dane_karty")
        self.column_names = [column[0] for column in cursor.fetchall()]

        sql = """SELECT ROW_NUMBER() OVER (ORDER BY id) AS numer,id, ReceiverCompanyName, TransporterCompanyName, CodeNumber, ProcessName, VehicleRegNumber, WasteMass, PlannedTransportTime, CertificateNumberAndBoxNumbers, AdditionalInfo FROM dane_karty WHERE creator = %s"""
        cursor.execute(sql, (self.creator,))

        rows = cursor.fetchall()
        for row in rows:
            modified_row = tuple(self.convert_date(value) for value in row)
            self.tree.insert('', 'end', values=modified_row)
        connection.close()

    @staticmethod
    def convert_date(value):

        if isinstance(value, str) and 'T' in value:
            try:

                date_str = value.split('.')[0].rstrip('Z')

                date_object = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")

                return date_object.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError as e:
                return value
        else:

            return value

    def delete_item(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Ostrzeżenie", "Proszę wybrać wiersz(e) do usunięcia")
            return

        response = messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz usunąć wybrane wiersze?")
        if not response:
            return

        connection = None
        try:
            connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password,
                                                 database=self.database)
            cursor = connection.cursor()
            for selected_item in selected_items:
                row_id = self.tree.item(selected_item, 'values')[1]
                cursor.execute("DELETE FROM dane_karty WHERE id = %s", (row_id,))
                self.tree.delete(selected_item)
            connection.commit()
            messagebox.showinfo("Informacja", "Wiersze zostały usunięte")
        except mysql.connector.Error as err:
            messagebox.showerror("Błąd", f"Wystąpił błąd: {err}")
        finally:
            if connection and connection.is_connected():
                connection.close()

    def on_item_double_click(self, event=None):
        selected_item = self.tree.selection()[0]
        row_id = self.tree.item(selected_item, 'values')[1]
        print("TO ROW ID" +str(row_id))

        connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password,
                                             database=self.database)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM dane_karty WHERE id = %s", (row_id,))
        row_data = cursor.fetchone()
        connection.close()

        if row_data:
            details = "\n".join([f"{col}: {val}" for col, val in zip(self.column_names, row_data)])
            messagebox.showinfo("Szczegóły", details)
        else:
            messagebox.showinfo("Informacja", "Nie znaleziono szczegółów dla wybranego wiersza.")

    def getelements(self, event = None):
        selected_item = self.tree.selection()[0]
        row_id = self.tree.item(selected_item, 'values')[1]

        connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password,
                                             database=self.database)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM dane_karty WHERE id = %s", (row_id,))
        row_data = cursor.fetchone()
        connection.close()
        if self.callback:
            self.callback(row_data)
        self.toplevel.destroy()

    def open_and_fetch_data(self):

        if not self.toplevel.winfo_exists():
            self.create_toplevel()
        else:
            self.load_data_from_db()