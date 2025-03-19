from tkinter import filedialog, messagebox
import os
import shutil
import KpoRequests

class PdfCreator:
    @staticmethod
    def gen_conf_card(tree, parent):
        selection = tree.selection()
        if selection:
            item = tree.item(selection, 'values')
            selected_id = item[0]
            file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], parent=parent)
            if file_path:
                disk_usage = shutil.disk_usage(os.path.dirname(file_path))
                free_space_gb = disk_usage.free / (1024 ** 3)

                if free_space_gb < 1:
                    messagebox.showwarning("Niewystarczająca przestrzeń",
                                           "Wybrana lokalizacja nie ma wystarczającej przestrzeni dyskowej. Wybierz inną lokalizację.")
                    return None
                else:
                    KpoRequests.KPO().wydruk(selected_id, file_path)
            else:
                return None

    @staticmethod
    def gen_conf(tree, parent):
        selection = tree.selection()
        if selection:
            item = tree.item(selection, 'values')
            selected_id = item[0]
            file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], parent=parent)
            if file_path:
                disk_usage = shutil.disk_usage(os.path.dirname(file_path))
                free_space_gb = disk_usage.free / (1024 ** 3)

                if free_space_gb < 1:
                    messagebox.showwarning("Niewystarczająca przestrzeń",
                                           "Wybrana lokalizacja nie ma wystarczającej przestrzeni dyskowej. Wybierz inną lokalizację.")
                    return None
                else:
                    KpoRequests.KPO().wydruk_karty(selected_id, file_path)
            else:
                return None