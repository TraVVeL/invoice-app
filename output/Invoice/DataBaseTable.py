from tkinter import ttk
import tkinter as tk
import os
from tkinter import messagebox
import sqlite3
from config import *

def sortby(tv, col, descending):
    data = [(tv.set(child, col), child) for child in tv.get_children('')]
    data.sort(reverse=descending)
    for index, item in enumerate(data):
        tv.move(item[1], '', index)
        tv.heading(col, command=lambda: sortby(tv, col, int(not descending)))


def show_table(frame, db_path, table_name, head):
    if os.path.isfile(db_path):
        with sqlite3.connect(db_path) as connection:
            cursor = connection.cursor()

            try:
                cursor.execute(f"SELECT * FROM {table_name}")
                rows_count = cursor.fetchone()[0]
            except sqlite3.OperationalError:
                rows_count = False

            if rows_count:
                cursor.execute(f"SELECT * FROM {table_name}")
                data = cursor.fetchall()
                # Создаем Treeview-виджет с горизонтальной и вертикальной прокруткой

                style = ttk.Style(frame)
                style.theme_use('alt')
                style.configure("Treeview", background='#242424', foreground='#fff', bordercolor='', font=font3)

                style.configure("Treeview.Heading", background=DARK_AQUA, foreground='#fff', bordercolor='#242424', font=font3)
                style.map("Treeview.Heading", background=[("active", GREEN)], foreground=[("active", "white")])

                table = ttk.Treeview(frame, show="headings", selectmode="browse")
                table["columns"] = head
                table["displaycolumns"] = head

                for head_row in head:
                    # Устанавливаем опцию stretch для каждого заголовка столбца
                    table.heading(head_row, text=head_row, anchor=tk.CENTER,
                                  command=lambda c=head_row: sortby(table, c, 0))
                    table.column(head_row, anchor=tk.CENTER, width=100, minwidth=50, stretch=True)
                for row in data:
                    table.insert('', tk.END, values=tuple(row))
                    table.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            else:
                messagebox.showinfo("Пустая таблица", "Таблица не содержит данных.")
    else:
        messagebox.showinfo("Пустая таблица", "Таблица не содержит данных.")
