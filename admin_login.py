import customtkinter as ctk
from config import *
from login import *


class Admin(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Авторизация")
        self.geometry('450x360')
        self.config()
        self.login()

    def login(self):
        frame2 = ctk.CTkFrame(self, width=470, height=360)
        frame2.place(x=0, y=0)

        login_label2 = ctk.CTkLabel(frame2, font=font1, text='Вход', width=200)
        login_label2.place(x=135, y=20)

        username_entry2 = ctk.CTkEntry(frame2, font=font2, border_width=3, placeholder_text='Логин', width=200,
                                       height=50)
        username_entry2.place(x=135, y=80)

        password_entry2 = ctk.CTkEntry(frame2, font=font2, show='*', border_width=3, placeholder_text='Пароль',
                                       width=200, height=50)
        password_entry2.place(x=135, y=150)

        login_button2 = ctk.CTkButton(frame2, font=font2, text='Войти', fg_color=DARK_AQUA, hover_color=GREEN,
                                      width=200, height=40,
                                      command=lambda: login_account(username_entry2, password_entry2,
                                                                    self.close_window))
        login_button2.place(x=135, y=220)

    def close_window(self):
        self.destroy()
