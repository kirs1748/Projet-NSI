from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk

def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.prettify()

# Chatgpt
class ScrollableKeyValueFrame(ttk.Frame):
    def __init__(self, parent, height=200):
        super().__init__(parent)

        self.canvas = tk.Canvas(self, height=height)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.inner_frame = ttk.Frame(self.canvas)
        self.window = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.inner_frame.bind("<Configure>", self._update_scroll)
        self.canvas.bind("<Configure>", self._resize)

        self.rows = []

        ttk.Label(self.inner_frame, text="Key").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(self.inner_frame, text="Value").grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.add_row()

    def _update_scroll(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _resize(self, event):
        self.canvas.itemconfig(self.window, width=event.width)

    def add_row(self):
        row = len(self.rows) + 1
        key = ttk.Entry(self.inner_frame)
        value = ttk.Entry(self.inner_frame)

        key.grid(row=row, column=0, padx=5, pady=2, sticky="ew")
        value.grid(row=row, column=1, padx=5, pady=2, sticky="ew")

        self.inner_frame.columnconfigure(0, weight=1)
        self.inner_frame.columnconfigure(1, weight=1)

        delete_btn = ttk.Button(self.inner_frame, text="❌", command=lambda r=row: self.delete_row(r))
        delete_btn.grid(row=row, column=2, padx=5, pady=2)

        self.rows.append({
            "key": key,
            "value": value,
            "button": delete_btn
        })

    def delete_row(self, row):
        if 0 < row <= len(self.rows):
            self.rows[row - 1]["key"].destroy()
            self.rows[row - 1]["value"].destroy()
            self.rows[row - 1]["button"].destroy()
            self.rows.pop(row - 1)
            for i in range(row - 1, len(self.rows)):
                self.rows[i]["key"].grid_configure(row=i + 1)
                self.rows[i]["value"].grid_configure(row=i + 1)
                self.rows[i]["button"].grid_configure(row=i + 1)


    def get_data(self):
        data = {}
        for row in self.rows:
            k = row["key"]
            v = row["value"]
            key = k.get().strip()
            value = v.get().strip()
            if key:
                data[key] = value
        return data
    
    def clear(self):
        for row in self.rows:
            row["key"].destroy()
            row["value"].destroy()
            row["button"].destroy()
        self.rows.clear()

    def load_data(self, data):
        self.clear()

        for key, value in data.items():
            self.add_row_with_data(key, value)

        # Toujours une ligne vide à la fin
        self.add_row()

    def add_row_with_data(self, key, value):
        self.add_row()
        self.rows[-1]["key"].insert(0, key)
        self.rows[-1]["value"].insert(0, value)
