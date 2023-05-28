from tkinter import messagebox
import admin_menu


def login_account(user_username, user_password, destroy_window):
    username = user_username.get()
    password = user_password.get()
    if username != '' and password != '':
        if username == 'admin':
            if password == 'admin':
                admin = admin_menu.App()
                destroy_window()
                admin.mainloop()
            else:
                messagebox.showerror('Ошибка', 'Пароль не верный')
        else:
            messagebox.showerror('Ошибка', 'Логин не верный')
    else:
        messagebox.showerror('Ошибка', 'Введите значения во все поля')