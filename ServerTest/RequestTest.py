import tkinter as tk
import HealthCheck
from datetime import datetime, timedelta
from tkinter import ttk

class RequestCheck:
    def __init__(self, container):
        self.container = container
        self.health_data = HealthCheck.HealthCheck()

    def HealthWindow(self):
        connection = self.health_data['Connection']
        date = self.health_data['Date']
        request_duration = self.health_data['request_duration']

        input_datetime = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %Z")
        hours_to_add = 1
        output_datetime = input_datetime + timedelta(hours=hours_to_add)
        date = output_datetime.strftime("%Y-%m-%d %H:%M:%S")

        if connection == "keep-alive":
            connection = "Serwer działa poprawnie"
        else:
            connection = "Błąd serwera"

        self.intercontainer = tk.Frame(self.container)
        self.intercontainer.pack(side="left")

        data = [("Status:", connection), ("Ostatnie zapytanie:", date), ("Czas odpowiedzi:", request_duration + " ms")]

        for i, (property, value) in enumerate(data):
            property_entry = ttk.Entry(self.intercontainer,width=22)
            property_entry.grid(row=i, column=0)
            property_entry.insert(tk.END, property)
            property_entry.config(state='readonly')

            value_entry = ttk.Entry(self.intercontainer,width=22)
            value_entry.grid(row=i, column=1)
            value_entry.insert(tk.END, value)
            value_entry.config(state='readonly')
        self.update_data()

    def update_data(self):
        self.health_data = HealthCheck.HealthCheck()

        connection = self.health_data['Connection']
        date = self.health_data['Date']
        request_duration = self.health_data['request_duration']

        input_datetime = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %Z")
        output_datetime = input_datetime + timedelta(hours=1)
        date = output_datetime.strftime("%Y-%m-%d %H:%M:%S")

        if connection == "keep-alive":
            connection = "Serwer działa poprawnie"
        else:
            connection = "Błąd serwera"

        property_entries = [child for child in self.intercontainer.winfo_children() if isinstance(child, ttk.Entry)]

        property_entries[1].config(state='normal')
        property_entries[1].delete(0, tk.END)
        property_entries[1].insert(tk.END, connection)
        property_entries[1].config(state='readonly')

        property_entries[3].config(state='normal')
        property_entries[3].delete(0, tk.END)
        property_entries[3].insert(tk.END, date)
        property_entries[3].config(state='readonly')

        property_entries[5].config(state='normal')
        property_entries[5].delete(0, tk.END)
        property_entries[5].insert(tk.END, request_duration + " ms")
        property_entries[5].config(state='readonly')

        self.container.after(1000, self.update_data)


if __name__ == '__main__':
    root = tk.Tk()
    container = tk.Frame(root)
    container.pack()
    RequestCheck(container).HealthWindow()
    root.mainloop()
