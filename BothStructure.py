import tkinter as tk
import csv
import bcrypt
from tkinter import messagebox

from tkinter import ttk
import string
from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import Error
from Globals import db_config


class DatabaseManager:
    def __init__(self, config, use_password):
        self.config = config.copy()
        if not use_password:
            self.config.pop('password', None)
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            self.cursor = self.connection.cursor()
            print("Połączenie testowe z bazą danych zostało nawiązane.")
            return True
        except Error as e:
            print(f"Błąd połączenia z bazą danych: {e}")
            return False

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Połączenie testowe z bazą danych zostało zamknięte.")



class DatabaseConnection:
    @staticmethod
    def connect():
        try:
            return mysql.connector.connect(**db_config)
        except Error as e:
            messagebox.showerror("Błąd połączenia z bazą danych", str(e))
            return None



class Options_reader:
    def __init__(self,file_path):
        self.file_path = file_path

    def read_csv_file_columns(self):
        try:
            with open(self.file_path, newline='', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=';')
                columns = [list(column) for column in zip(*reader)]
            return columns
        except FileNotFoundError:
            print(f"File not found: {self.file_path}")
            return None



class UserLoader:
    @staticmethod
    def load_users():
        conn = DatabaseConnection.connect()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("SELECT Login, Haslo FROM Data_user")
            users = {login: password for login, password in cursor.fetchall()}
            conn.close()
            return users
        return {}


class Structure:
    @staticmethod
    def create_structure():
        root = tk.Tk()
        root.state("zoomed")
        container = tk.Frame(root)
        container.place(relx=0.5, rely=0.5, anchor="center")
        custom_font = ("Helvetica", 12)
        label1 = tk.Label(container, font=custom_font, text="Login:")
        label1.grid(row=0, column=0, pady=3)
        entry1 = tk.Entry(container, font=custom_font)
        entry1.grid(row=0, column=1, pady=3)

        label2 = tk.Label(container, font=custom_font, text="Hasło:")
        label2.pack()
        entry2 = tk.Entry(container, font=custom_font, show="*")
        entry2.pack()
        toggle_button = tk.Button(
            container,
            font=custom_font,
            text="Pokaż hasło",
            command=lambda: Structure.toggle_visibility(entry2),
        )
        toggle_button.pack()

    @staticmethod
    def toggle_visibility(entry2):
        current_state = entry2.cget("show")
        new_state = "" if current_state == "*" else "*"
        entry2.config(show=new_state)

class Tooltip:
    def __init__(self, master, text):
        self.master = master
        self.tooltip_window = None
        self.text = text

    def show_tooltip(self):
        x, y, _, _ = self.master.bbox("insert")
        x += self.master.winfo_rootx() + 25
        y += self.master.winfo_rooty() + 25

        if self.tooltip_window:
            self.tooltip_window.destroy()

        self.tooltip_window = tk.Toplevel(self.master)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            self.tooltip_window,
            text=self.text,
            justify="left",
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
        )
        label.pack(ipadx=1)

        label.bind("<Leave>", self.hide_tooltip)

    def hide_tooltip(self, _):
        if self.tooltip_window:
            self.tooltip_window.destroy()


class Root:
    @staticmethod
    def root():
        root = tk.Tk()
        return root


class ContextMenuHandler:
    def __init__(self, master):
        self.master = master
        self.context_menu = tk.Menu(master, tearoff=0)
        self.context_menu.add_command(label="Kopiuj", command=self.copy_action)
        self.context_menu.add_command(label="Wklej", command=self.paste_action)

        master.bind("<Button-3>", self.on_right_click)

    def on_right_click(self, event):
        current_focus = self.master.focus_get()
        if isinstance(current_focus, tk.Entry):
            self.context_menu.post(event.x_root, event.y_root)

    def copy_action(self):
        selected_text = self.get_selected_text()
        if selected_text:
            self.master.clipboard_clear()
            self.master.clipboard_append(selected_text)
            self.master.update()

    def paste_action(self):
        current_focus = self.master.focus_get()
        if isinstance(current_focus, tk.Entry):
            clipboard_text = self.master.clipboard_get()
            if clipboard_text:
                current_focus.insert(tk.END, clipboard_text)

    def get_selected_text(self):
        current_focus = self.master.focus_get()
        if isinstance(current_focus, tk.Entry):
            return (
                current_focus.selection_get()
                if current_focus.selection_present()
                else None
            )
        else:
            return None


class ButtonWithColorChange:
    def __init__(self, master):
        self.master = master
        self.button = tk.Button(
            master,
            text="Przycisk",
            command=self.on_button_click,
            activebackground="red",
            activeforeground="white",
        )
        self.button.pack()

    @staticmethod
    def on_button_click():
        print("Przycisk został wciśnięty")


class Password:
    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_password

    @staticmethod
    def verify_password(password, hashed_password):
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password)

    @staticmethod
    def start_code(pw_entry):
        password = pw_entry.get()
        has_required_length = len(password) >= 6
        has_uppercase = any(char.isupper() for char in password)
        has_special_character = any(char in string.punctuation for char in password)

        requirements = []

        if not has_required_length:
            requirements.append("Min. 6 znaków")

        if not has_uppercase:
            requirements.append("Wielka litera")

        if not has_special_character:
            requirements.append("Znak specjalny")

        return requirements


class RoundedButton(ttk.Button):
    def __init__(self, master=None, **kwargs):
        ttk.Button.__init__(self, master, style="Rounded.TButton", **kwargs)


class RoundedStyle:
    @staticmethod
    def apply_rounded_style(button):
        style = ttk.Style()

        style.configure(
            "Rounded.TButton",
            padding=3,
            relief="flat",
            background="#ccc",
            borderwidth=1,
            bordercolor="#999",
            focusthickness=3,
            focuscolor="#aaa",
            highlightthickness=0,
            anchor="center",
            font=("Helvetica", 12),
        )

        button.configure(style="Rounded.TButton")


class Logout:
    def __init__(self, container, row, column, width, session, main_root):
        self.container = container
        self.row = row
        self.column = column
        self.width = width
        self.session = session
        self.main_root = main_root

    def logout_button(self):
        button = RoundedButton(
            self.container,
            text="Wyloguj",
            width=self.width,
            command=lambda: self.on_close(),
        )
        button.grid(row=self.row, column=self.column, padx=4, sticky="n")

    def on_close(self):
        self.main_root.destroy()
        self.session.end_session()



class SessionLogger:

    @staticmethod
    def seconds_to_hms(seconds):
        return str(timedelta(seconds=seconds))

    session_counter = 0

    def __init__(self, call, user):
        SessionLogger.session_counter += 1
        self.session_number = SessionLogger.session_counter
        self.call = call
        self.logged_in = False
        self.session_data = []
        self.user = user
        self.login_time = None

    def login(self):
        if not self.logged_in:
            self.logged_in = True
            self.start_session()
        else:
            messagebox.showerror("Błąd logowania", "Jesteś już zalogowany")

    def start_session(self):
        user_login = self.user
        self.login_time = datetime.now()
        login_time_str = self.login_time.strftime("%Y-%m-%d %H:%M:%S")
        self.session_data.append(
            {
                "UserLogin": user_login,
                "LoginTime": login_time_str,
                "LogoutTime": "",
                "Duration": "",
            }
        )


    def end_session(self):
        if self.logged_in:
            logout_time = datetime.now()
            duration = int((logout_time - self.login_time).total_seconds())
            current_session = self.session_data[-1]
            current_session["LogoutTime"] = logout_time.strftime("%Y-%m-%d %H:%M:%S")
            current_session["Duration"] = SessionLogger.seconds_to_hms(duration)

            self.save_session_data()

            self.logged_in = False

    def save_session_data(self):
        conn = DatabaseConnection.connect()
        if conn is not None:
            cursor = conn.cursor()
            session = self.session_data[-1]
            cursor.execute(
                "INSERT INTO session_Log (Login, Start, Koniec, Czas_sesji) VALUES (%s, %s, %s, %s)",
                (session["UserLogin"], session["LoginTime"], session["LogoutTime"], session["Duration"])
            )
            conn.commit()
            conn.close()

class Errors:
    def database_error(self):
        messagebox.showerror("ERROR","Błąd bazy danych")

class CopyAndPaste:
    def __init__(self, treeview, root):
        self.treeview = treeview
        self.root = root
        self.selected_column = None
        self._create_context_menu()

    def _create_context_menu(self):
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Kopiuj wiersz", command=self._copy_row_to_clipboard)
        self.context_menu.add_command(label="Kopiuj pole", command=self._copy_field_to_clipboard)
        self.treeview.bind("<Button-3>", self._on_treeview_right_click)

    def _copy_row_to_clipboard(self):
        selected_item = self.treeview.selection()
        if selected_item:
            item = self.treeview.item(selected_item[0])
            values = item['values']
            row_to_copy = "\t".join(map(str, values))
            self.root.clipboard_clear()
            self.root.clipboard_append(row_to_copy)

    def _copy_field_to_clipboard(self):
        selected_item = self.treeview.selection()
        if selected_item and self.selected_column is not None:
            item = self.treeview.item(selected_item[0])

            column_index = int(self.selected_column.replace('#', '')) - 1
            value = item['values'][column_index]
            self.root.clipboard_clear()
            self.root.clipboard_append(value)

    def _on_treeview_right_click(self, event):
        region = self.treeview.identify("region", event.x, event.y)
        if region == "cell":
            row_id = self.treeview.identify_row(event.y)
            self.selected_column = self.treeview.identify_column(event.x)
            if row_id:
                self.treeview.selection_set(row_id)
                self.context_menu.entryconfig("Kopiuj pole", state="normal")
            else:
                self.context_menu.entryconfig("Kopiuj pole", state="disabled")
        else:
            self.selected_column = None
            self.context_menu.entryconfig("Kopiuj pole", state="disabled")

        if self.treeview.selection():
            self.context_menu.post(event.x_root, event.y_root)

class CenterWindow:
    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_reqwidth()
        height = window.winfo_reqheight()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2) - 80)
        window.geometry(f'{width}x{height}+{x}+{y}')




if __name__ == "__main__":
    Structure.create_structure()
