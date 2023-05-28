# -*- coding: utf-8 -*-
"""
Для разработки бизнес-процессов обработки счета-фактуры продукта, необходимо выполнить следующие шаги:


Получение счета-фактуры: необходимо определить и документально оформить процедуру получения счета-фактуры от поставщика.
Это может быть выполнено путем организации электронной системы обмена документами, либо посредством традиционного
способа - почтовой или курьерской доставки.

Проверка счета-фактуры: проверка счета-фактуры является важным этапом в процессе его обработки.

Оплата счета-фактуры: после проверки счета-фактуры необходимо произвести оплату счета-фактуры в соответствии с
условиями договора. Для этого могут использоваться различные методы оплаты, такие как банковский перевод, электронные
платежи или чек.

Оптимизация процессов: после проведения первых этапов процесса разработки бизнес-процессов обработки счета-фактуры
продукта, необходимо провести анализ результатов и определить возможности для оптимизации процедур. Это может включать в
себя автоматизацию отдельных шагов, сокращение времени выполнения операций и т.д.
"""

import tkinter
import tkinter.messagebox
from tkinter import messagebox

import customtkinter as Ctk
from data_base import *
from validation import Validator
from xlsfiller import XlsFiller
from data_config import *
import admin_login



Ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
Ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue,GREEN



class App(Ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.resizable(False, False)
        self.valid_mail = (None, None)
        self.valid_cvv = (None, None)
        self.valid_card_data = (None, None)
        self.valid_card_number = (None, None)
        self.valid_surname = (None, None)
        self.valid_name = (None, None)

        self.get_value = {}

        # configure window
        self.valid_percent_1 = (None, None)
        self.valid_digit_1 = (None, None)
        self.valid_digit_2 = (None, None)
        self.valid_date = (None, None)
        self.valid_full_name = (None, None)
        self.valid_inn_kpp = (None, None)
        self.valid_percent_2 = (None, None)
        self.valid_digit_3 = (None, None)

        self.title("Получение счета-фактуры")
        self.geometry(f"{1100}x{580}")

        # create login frame
        self.login_frame = Ctk.CTkFrame(self)
        self.login_frame.place(relx=0, rely=0)

        self.login_label = Ctk.CTkBaseClass(self.login_frame)
        self.login_label.grid(padx=550, pady=290)

        # create main frame
        self.main_frame = Ctk.CTkFrame(self)
        self.main_label = Ctk.CTkBaseClass(self.main_frame)
        self.main_label.grid(padx=500, pady=300)

        # Здесь мы создаем обработчик событий клавиатуры для клавиши F1
        self.bind("<F1>", self.admin_login_handler)


        #
        # Adding main text
        font = Ctk.CTkFont(size=FONT_SIZE)
        self.text_main = Ctk.CTkLabel(self.login_frame, text='Заполнение счёта-фактуры')
        self.text_main.configure(self.login_frame, font=font)
        self.text_main.place(relx=0.5, rely=0.05, anchor=tkinter.CENTER)

        # LABEL 1
        #
        self.bfe_label = Ctk.CTkLabel(self.login_frame, text='ИНН/КПП покупателя')
        self.bfe_label.place(rely=0.12 + label_y, relx=0.09 + label_x)
        self.entry_fill_inn = Ctk.CTkEntry(self.login_frame, placeholder_text='ИНН/КПП', width=entry_w, height=entry_h)
        self.entry_fill_inn.place(rely=0.2 + entry_y, relx=0.2 + entry_x, anchor=tkinter.CENTER)
        self.entry_fill_inn.bind("<KeyRelease>", lambda event: self.check_input1(self.entry_fill_inn.get()))

        #
        #
        self.bfe_label = Ctk.CTkLabel(self.login_frame, text='Текущая дата')
        self.bfe_label.place(rely=0.24 + label_y, relx=0.09 + label_x)
        self.entry_fill_date = Ctk.CTkEntry(self.login_frame, height=entry_h, width=entry_w,
                                            placeholder_text='__.__.__')
        self.entry_fill_date.place(rely=0.32 + entry_y, relx=0.2 + entry_x, anchor=tkinter.CENTER)
        self.entry_fill_date.bind("<KeyRelease>", lambda event: self.check_input2(self.entry_fill_date.get()))

        #
        #
        self.bfe_label = Ctk.CTkLabel(self.login_frame, text='Фамилия, имя, отчество')
        self.bfe_label.place(rely=0.36 + label_y, relx=0.09 + label_x)
        self.entry_fill_full_name = Ctk.CTkEntry(self.login_frame, height=entry_h, width=entry_w,
                                                 placeholder_text='ФИО')
        self.entry_fill_full_name.place(rely=0.44 + entry_y, relx=0.2 + entry_x, anchor=tkinter.CENTER)
        self.entry_fill_full_name.bind("<KeyRelease>", lambda event: self.check_input3(self.entry_fill_full_name.get()))

        #
        #
        self.bfe_label = Ctk.CTkLabel(self.login_frame, text='Код')
        self.bfe_label.place(rely=0.48 + label_y, relx=0.09 + label_x)
        self.entry_fill_code = Ctk.CTkEntry(self.login_frame, height=entry_h, width=entry_w, placeholder_text='Код')
        self.entry_fill_code.place(rely=0.56 + entry_y, relx=0.2 + entry_x, anchor=tkinter.CENTER)
        self.entry_fill_code.bind("<KeyRelease>", lambda event: self.check_input4(self.entry_fill_code.get()))

        #
        #
        self.bfe_label = Ctk.CTkLabel(self.login_frame, text='Кол-во')
        self.bfe_label.place(rely=0.60 + label_y, relx=0.09 + label_x)
        self.entry_fill_code_amount = Ctk.CTkEntry(self.login_frame, height=entry_h, width=entry_w,
                                                   placeholder_text='Кол-во')
        self.entry_fill_code_amount.place(rely=0.68 + entry_y, relx=0.2 + entry_x, anchor=tkinter.CENTER)
        self.entry_fill_code_amount.bind("<KeyRelease>",
                                         lambda event: self.check_input5(self.entry_fill_code_amount.get()))

        #
        #
        self.bfe_label = Ctk.CTkLabel(self.login_frame, text='Цена')
        self.bfe_label.place(rely=0.72 + label_y, relx=0.09 + label_x)
        self.entry_fill_price_by_unit = Ctk.CTkEntry(self.login_frame, height=entry_h, width=entry_w,
                                                     placeholder_text='Цена за единицу товара')
        self.entry_fill_price_by_unit.place(rely=0.80 + entry_y, relx=0.2 + entry_x, anchor=tkinter.CENTER)
        self.entry_fill_price_by_unit.bind("<KeyRelease>",
                                           lambda event: self.check_input6(self.entry_fill_price_by_unit.get()))

        #
        #
        self.bfe_label = Ctk.CTkLabel(self.login_frame, text='Акцизы')
        self.bfe_label.place(rely=0.84 + label_y, relx=0.09 + label_x)
        self.entry_fill_excise = Ctk.CTkEntry(self.login_frame, height=entry_h, width=entry_w,
                                              placeholder_text='Акцизы')
        self.entry_fill_excise.place(rely=0.92 + entry_y, relx=0.2 + entry_x, anchor=tkinter.CENTER)
        self.entry_fill_excise.bind("<KeyRelease>", lambda event: self.check_input7(self.entry_fill_excise.get()))

        #
        #
        self.bfe_label = Ctk.CTkLabel(self.login_frame, text='Налог')
        self.bfe_label.place(rely=0.12 + label_y, relx=0.49 + label_x)
        self.entry_fill_tax = Ctk.CTkEntry(self.login_frame, height=entry_h, width=entry_w, placeholder_text='Налог')
        self.entry_fill_tax.place(rely=0.2 + entry_y, relx=0.6 + entry_x, anchor=tkinter.CENTER)
        self.entry_fill_tax.bind("<KeyRelease>", lambda event: self.check_input8(self.entry_fill_tax.get()))

        #
        # USER SIGNATURE AND HIS FULL NAME
        self.bfe_label = Ctk.CTkLabel(self.login_frame, text='Подпись или своё имя')
        self.bfe_label.place(rely=0.24 + label_y, relx=0.49 + label_x)
        self.entry_fill_signature = Ctk.CTkEntry(self.login_frame, height=entry_h, width=entry_w,
                                                 placeholder_text='Иванов')
        self.entry_fill_signature.place(rely=0.32 + entry_y, relx=0.6 + entry_x, anchor=tkinter.CENTER)

        #
        #
        self.bfe_label = Ctk.CTkLabel(self.login_frame, text='Номер договора')
        self.bfe_label.place(rely=0.36 + label_y, relx=0.49 + label_x)
        self.entry_fill_bill = Ctk.CTkEntry(self.login_frame, height=entry_h, width=entry_w,
                                            placeholder_text='№ Договора')
        self.entry_fill_bill.place(rely=0.44 + entry_y, relx=0.6 + entry_x, anchor=tkinter.CENTER)

        #
        #
        self.bfe_label = Ctk.CTkLabel(self.login_frame, text='ИНН\\КПП покупателя')
        self.bfe_label.place(rely=0.48 + label_y, relx=0.49 + label_x)
        self.entry_fill_sender = Ctk.CTkEntry(self.login_frame, height=entry_h, width=entry_w,
                                              placeholder_text='Отправитель')
        self.entry_fill_sender.place(rely=0.56 + entry_y, relx=0.6 + entry_x, anchor=tkinter.CENTER)

        #
        #
        self.bfe_label = Ctk.CTkLabel(self.login_frame, text=f"Грузополучатель\\его адрес")
        self.bfe_label.place(rely=0.60 + label_y, relx=0.49 + label_x)
        self.entry_fill_receiver = Ctk.CTkEntry(self.login_frame, height=entry_h, width=entry_w,
                                                placeholder_text='Получатель')
        self.entry_fill_receiver.place(rely=0.68 + entry_y, relx=0.6 + entry_x, anchor=tkinter.CENTER)

        #
        #
        self.bfe_label = Ctk.CTkLabel(self.login_frame, text='Покупатель')
        self.bfe_label.place(rely=0.72 + label_y, relx=0.49 + label_x)
        self.entry_fill_buyer = Ctk.CTkEntry(self.login_frame, height=entry_h, width=entry_w,
                                             placeholder_text='ООО "ПОКУПАТЕЛЬ"')
        self.entry_fill_buyer.place(rely=0.80 + entry_y, relx=0.6 + entry_x, anchor=tkinter.CENTER)

        #
        #
        self.button = Ctk.CTkButton(self.login_frame, height=40, width=250, text="Вывести фактуру",
                                    command=self.login_event)
        self.button.place(rely=0.92, relx=0.6 + entry_x, anchor=tkinter.CENTER)

        #   LABEL 1 ERRORS
        #
        self.error_fill_inn = Ctk.CTkLabel(self.login_frame, text='')
        self.error_fill_inn.place(rely=0.2 + error_y, relx=0.38 + error_x, anchor=tkinter.CENTER)

        self.error_fill_date = Ctk.CTkLabel(self.login_frame, text='')
        self.error_fill_date.place(rely=0.32 + error_y, relx=0.38 + error_x, anchor=tkinter.CENTER)

        self.error_fill_full_name = Ctk.CTkLabel(self.login_frame, text='')
        self.error_fill_full_name.place(rely=0.44 + error_y, relx=0.38 + error_x, anchor=tkinter.CENTER)

        self.error_fill_code = Ctk.CTkLabel(self.login_frame, text='')
        self.error_fill_code.place(rely=0.56 + error_y, relx=0.38 + error_x, anchor=tkinter.CENTER)

        self.error_fill_code_amount = Ctk.CTkLabel(self.login_frame, text='')
        self.error_fill_code_amount.place(rely=0.68 + error_y, relx=0.38 + error_x, anchor=tkinter.CENTER)

        self.error_fill_price_by_unit = Ctk.CTkLabel(self.login_frame, text='')
        self.error_fill_price_by_unit.place(rely=0.8 + error_y, relx=0.38 + error_x, anchor=tkinter.CENTER)

        self.error_fill_excise = Ctk.CTkLabel(self.login_frame, text='')
        self.error_fill_excise.place(rely=0.92 + error_y, relx=0.38 + error_x, anchor=tkinter.CENTER)

        self.error_fill_tax = Ctk.CTkLabel(self.login_frame, text='')
        self.error_fill_tax.place(rely=0.2 + error_y, relx=0.78 + error_x, anchor=tkinter.CENTER)

        #   LABEL 2
        #   LABEL 2
        #   LABEL 2
        #   LABEL 2

        font = Ctk.CTkFont(size=50)
        self.text_main = Ctk.CTkLabel(self.main_frame, text='Оплата')
        self.text_main.configure(self.main_frame, font=font)
        self.text_main.place(relx=0.5, rely=0.05, anchor=tkinter.CENTER)
        #
        #

        #
        #
        self.bfe_label = Ctk.CTkLabel(self.main_frame, text='Имя ')
        self.bfe_label.place(rely=0.12 + label_y, relx=0.255 + label_x)
        self.entry_fill_name = Ctk.CTkEntry(self.main_frame, placeholder_text='Ivan', width=300, height=entry_h)
        self.entry_fill_name.place(rely=0.2 + entry_y, relx=0.4 + entry_x, anchor=tkinter.CENTER)
        self.entry_fill_name.bind("<KeyRelease>", lambda event: self.check_input_2_1(self.entry_fill_name.get()))

        #
        #
        self.bfe_label = Ctk.CTkLabel(self.main_frame, text='Фамилия')
        self.bfe_label.place(rely=0.27 + label_y, relx=0.255 + label_x)
        self.entry_fill_surname = Ctk.CTkEntry(self.main_frame, placeholder_text='Ivanov', width=300, height=entry_h)
        self.entry_fill_surname.place(rely=0.35 + entry_y, relx=0.4 + entry_x, anchor=tkinter.CENTER)
        self.entry_fill_surname.bind("<KeyRelease>", lambda event: self.check_input_2_2(self.entry_fill_surname.get()))

        #
        #
        self.bfe_label = Ctk.CTkLabel(self.main_frame, text='Номер карты')
        self.bfe_label.place(rely=0.42 + label_y, relx=0.255 + label_x)
        self.entry_fill_card = Ctk.CTkEntry(self.main_frame, placeholder_text='XXXX-XXXX-XXXX-XXXX', width=300,
                                            height=entry_h)
        self.entry_fill_card.place(rely=0.50 + entry_y, relx=0.4 + entry_x, anchor=tkinter.CENTER)
        self.entry_fill_card.bind("<KeyRelease>", lambda event: self.check_input_2_3(self.entry_fill_card.get()))

        #
        #
        self.bfe_label = Ctk.CTkLabel(self.main_frame, text='Дата')
        self.bfe_label.place(rely=0.57 + label_y, relx=0.255 + label_x)
        self.entry_fill_card_date = Ctk.CTkEntry(self.main_frame, height=entry_h, width=140,
                                                 placeholder_text='__.__.__')
        self.entry_fill_card_date.place(rely=0.65 + entry_y, relx=0.32 + entry_x, anchor=tkinter.CENTER)
        self.entry_fill_card_date.bind("<KeyRelease>",
                                       lambda event: self.check_input_2_4(self.entry_fill_card_date.get()))

        #
        #
        self.bfe_label = Ctk.CTkLabel(self.main_frame, text='СVV')
        self.bfe_label.place(rely=0.57 + label_y, relx=0.41 + label_x)
        self.entry_fill_cvv = Ctk.CTkEntry(self.main_frame, show="*", height=entry_h, width=140,
                                           placeholder_text='***')
        self.entry_fill_cvv.place(rely=0.65 + entry_y, relx=0.48 + entry_x, anchor=tkinter.CENTER)
        self.entry_fill_cvv.bind("<KeyRelease>", lambda event: self.check_input_2_5(self.entry_fill_cvv.get()))

        #
        #
        self.bfe_label = Ctk.CTkLabel(self.main_frame, text='E-mail')
        self.bfe_label.place(rely=0.72 + label_y, relx=0.255 + label_x)
        self.entry_fill_mail = Ctk.CTkEntry(self.main_frame, placeholder_text='triplez@gmail.com', width=300,
                                            height=entry_h)
        self.entry_fill_mail.place(rely=0.80 + entry_y, relx=0.4 + entry_x, anchor=tkinter.CENTER)
        self.entry_fill_mail.bind("<KeyRelease>", lambda event: self.check_input_2_6(self.entry_fill_mail.get()))

        self.make_transaction = Ctk.CTkButton(self.main_frame, height=40, width=190, text="Произвести транзакцию",
                                              command=self.final_event, fg_color=GREEN, hover_color='gray')
        self.make_transaction.place(rely=0.90, relx=0.455 + entry_x, anchor=tkinter.CENTER)

        self.back_button = Ctk.CTkButton(self.main_frame, height=40, width=90, text="Назад",
                                         command=self.back_event)
        self.back_button.place(rely=0.90, relx=0.295 + entry_x, anchor=tkinter.CENTER)

        #    LABEL 2 ERRORS
        #
        self.error_fill_name = Ctk.CTkLabel(self.login_frame, text='')
        self.error_fill_name.place(rely=0.2 + error_y, relx=0.38 + error_x, anchor=tkinter.CENTER)

        self.error_fill_surname = Ctk.CTkLabel(self.login_frame, text='')
        self.error_fill_surname.place(rely=0.2 + error_y, relx=0.38 + error_x, anchor=tkinter.CENTER)

        self.error_fill_card = Ctk.CTkLabel(self.login_frame, text='')
        self.error_fill_card.place(rely=0.2 + error_y, relx=0.38 + error_x, anchor=tkinter.CENTER)

        self.error_fill_card_date = Ctk.CTkLabel(self.login_frame, text='')
        self.error_fill_card_date.place(rely=0.2 + error_y, relx=0.38 + error_x, anchor=tkinter.CENTER)

        self.error_fill_cvv = Ctk.CTkLabel(self.login_frame, text='')
        self.error_fill_cvv.place(rely=0.2 + error_y, relx=0.38 + error_x, anchor=tkinter.CENTER)

        self.error_fill_mail = Ctk.CTkLabel(self.login_frame, text='')
        self.error_fill_mail.place(rely=0.2 + error_y, relx=0.38 + error_x, anchor=tkinter.CENTER)

    def login_event(self):
        entries = [self.valid_inn_kpp, self.valid_date, self.valid_full_name,
                   self.valid_digit_1, self.valid_digit_2, self.valid_digit_3,
                   self.valid_percent_1, self.valid_percent_2]

        values = [self.entry_fill_inn.get(), self.entry_fill_date.get(), self.entry_fill_full_name.get(),
                  self.entry_fill_code.get(), self.entry_fill_code_amount.get(), self.entry_fill_price_by_unit.get(),
                  self.entry_fill_excise.get(), self.entry_fill_tax.get(),
                  self.entry_fill_signature.get(), self.entry_fill_bill.get(), self.entry_fill_sender.get(),
                  self.entry_fill_receiver.get(), self.entry_fill_buyer.get()]



        self.get_value = {k: v for k, v in zip(keys, values)}

        get_boolean = [tof[0] for tof in entries]

        if all(get_boolean):
            self.login_frame.grid_forget()  # remove login frame
            self.main_frame.grid(row=0, column=0, sticky="nsew", padx=100)  # show main frame

        else:
            messagebox.showinfo("Ошибка ввода", "Есть незаполненные поля")

    def final_event(self):
        user_mail = self.entry_fill_mail.get()
        entries = [self.valid_surname, self.valid_name, self.valid_card_number,
                   self.valid_card_data, self.valid_cvv, self.valid_mail]
        values = [self.entry_fill_name.get(), self.entry_fill_surname.get(), self.entry_fill_card.get(),
                  self.entry_fill_card_date.get(), self.entry_fill_cvv.get(), self.entry_fill_mail.get()]
        get_boolean = [tof[0] for tof in entries]

        if all(get_boolean):

            messagebox.showinfo("Успех", "счёт-фактуры будет отправлен на указанную почту")
            XlsFiller().call_event_to_fill_the_blank(USER_BILL=self.get_value, USER_MAIL=user_mail)

            
            cursor.execute('''INSERT INTO user_data (name, surname, card, date_exp, card_cvv, email) 
            VALUES (?, ?, ?, ?, ?, ?)''', tuple(values))

            cursor.execute('''INSERT INTO facture (
            inn, current_date, full_name, code, amount, price, excise, tax, signature, 
            contract_number, inn_buyer, sender, buyer) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', tuple(values))
            conn.commit()

            conn.commit()
            conn.close()
        else:
            messagebox.showinfo("Ошибка вода", "Есть незаполненные поля")

    def back_event(self):
        self.main_frame.grid_forget()  # remove main frame
        self.login_frame.grid(row=0, column=0, sticky="ns")  # show login frame

    def check_input1(self, inn_kpp):

        self.valid_inn_kpp = Validator().is_inn_kpp(inn_kpp), inn_kpp
        if self.valid_inn_kpp[0]:
            self.entry_fill_inn.configure(border_color=GREEN, text_color=GREEN)
            self.error_fill_inn.configure(text="")
        else:
            self.entry_fill_inn.configure(border_color=MAIN_COLOR, text_color=MAIN_COLOR,
                                          bg_color='transparent')
            self.error_fill_inn.configure(text="КПП\\КПП некорректны")

    def check_input2(self, date):
        self.valid_date = Validator().is_date(date), date
        if self.valid_date[0]:
            self.entry_fill_date.configure(border_color=GREEN, text_color=GREEN)
            self.error_fill_date.configure(text="")
        else:
            self.entry_fill_date.configure(border_color=MAIN_COLOR, text_color=MAIN_COLOR)
            self.error_fill_date.configure(text="Дата указана не верно")

    def check_input3(self, full_name):

        self.valid_full_name = Validator().is_fullname(full_name), full_name
        if self.valid_full_name[0]:
            self.entry_fill_full_name.configure(border_color=GREEN, text_color=GREEN)
            self.error_fill_full_name.configure(text="")
        else:
            self.entry_fill_full_name.configure(border_color=MAIN_COLOR, text_color=MAIN_COLOR)
            self.error_fill_full_name.configure(text="Не соответствует ФИО")

    def check_input4(self, digit_1):

        self.valid_digit_1 = Validator().is_number(digit_1), digit_1
        if self.valid_digit_1[0]:
            self.entry_fill_code.configure(border_color=GREEN, text_color=GREEN)
            self.error_fill_code.configure(text="")
        else:
            self.entry_fill_code.configure(border_color=MAIN_COLOR, text_color=MAIN_COLOR)
            self.error_fill_code.configure(text="Введите число            ")

    def check_input5(self, digit2):

        self.valid_digit_2 = Validator().is_number(digit2), digit2
        if self.valid_digit_2[0]:
            self.entry_fill_code_amount.configure(border_color=GREEN, text_color=GREEN)
            self.error_fill_code_amount.configure(text="")
        else:
            self.entry_fill_code_amount.configure(border_color=MAIN_COLOR, text_color=MAIN_COLOR)
            self.error_fill_code_amount.configure(text="Введите число            ")

    def check_input6(self, digit3):

        self.valid_digit_3 = Validator().is_number(digit3), digit3
        if self.valid_digit_3[0]:
            self.entry_fill_price_by_unit.configure(border_color=GREEN, text_color=GREEN)
            self.error_fill_price_by_unit.configure(text="")
        else:
            self.entry_fill_price_by_unit.configure(border_color=MAIN_COLOR, text_color=MAIN_COLOR)
            self.error_fill_price_by_unit.configure(text="Введите число            ")

    def check_input7(self, percent_1):

        self.valid_percent_1 = Validator().is_percent(percent_1), percent_1
        if self.valid_percent_1[0]:
            self.entry_fill_excise.configure(border_color=GREEN, text_color=GREEN)
            self.error_fill_excise.configure(text="")
        else:
            self.entry_fill_excise.configure(border_color=MAIN_COLOR, text_color=MAIN_COLOR)
            self.error_fill_excise.configure(text="Введите процент         ")

    def check_input8(self, percent_2):
        self.valid_percent_2 = Validator().is_percent(percent_2), percent_2
        if self.valid_percent_2[0]:
            self.entry_fill_tax.configure(border_color=GREEN, text_color=GREEN)
            self.error_fill_tax.configure(text="")
        else:
            self.entry_fill_tax.configure(border_color=MAIN_COLOR, text_color=MAIN_COLOR)
            self.error_fill_tax.configure(text="Введите процент         ")

    def check_input_2_1(self, name):
        self.valid_name = Validator().is_name(name), name
        if self.valid_name[0]:
            self.entry_fill_name.configure(border_color=GREEN, text_color=GREEN)
            self.error_fill_name.configure(text="")
        else:
            self.entry_fill_name.configure(border_color=MAIN_COLOR, text_color=MAIN_COLOR)
            self.error_fill_name.configure(text="Введите процент         ")

    def check_input_2_2(self, surname):
        self.valid_surname = Validator().is_name(surname), surname
        if self.valid_surname[0]:
            self.entry_fill_surname.configure(border_color=GREEN, text_color=GREEN)
            self.error_fill_surname.configure(text="")
        else:
            self.entry_fill_surname.configure(border_color=MAIN_COLOR, text_color=MAIN_COLOR)
            self.error_fill_surname.configure(text="Введите процент         ")

    def check_input_2_3(self, card_number):
        self.valid_card_number = Validator().is_valid_credit_card_number(card_number), card_number
        if self.valid_card_number[0]:
            self.entry_fill_card.configure(border_color=GREEN, text_color=GREEN)
            self.error_fill_card.configure(text="")
        else:
            self.entry_fill_card.configure(border_color=MAIN_COLOR, text_color=MAIN_COLOR)
            self.error_fill_card.configure(text="Введите процент         ")

    def check_input_2_4(self, card_data):
        self.valid_card_data = Validator().is_valid_credit_card_date(card_data), card_data
        if self.valid_card_data[0]:
            self.entry_fill_card_date.configure(border_color=GREEN, text_color=GREEN)
            self.error_fill_card_date.configure(text="")
        else:
            self.entry_fill_card_date.configure(border_color=MAIN_COLOR, text_color=MAIN_COLOR)
            self.error_fill_card_date.configure(text="Введите процент         ")

    def check_input_2_5(self, cvv):
        self.valid_cvv = Validator().is_valid_cvv(cvv), cvv
        if self.valid_cvv[0]:
            self.entry_fill_cvv.configure(border_color=GREEN, text_color=GREEN)
            self.error_fill_cvv.configure(text="")
        else:
            self.entry_fill_cvv.configure(border_color=MAIN_COLOR, text_color=MAIN_COLOR)
            self.error_fill_cvv.configure(text="Введите процент         ")

    def check_input_2_6(self, mail):
        self.valid_mail = Validator().is_valid_email(mail), mail
        if self.valid_mail[0]:
            self.entry_fill_mail.configure(border_color=GREEN, text_color=GREEN)
            self.error_fill_mail.configure(text="")
        else:
            self.entry_fill_mail.configure(border_color=MAIN_COLOR, text_color=MAIN_COLOR)
            self.error_fill_mail.configure(text="Введите процент         ")

    def admin_login_handler(self, event):
        # Обработчик событий, который вызывает функцию из модуля admin_login при нажатии клавиши F1
        admin = admin_login.Admin()
        admin.mainloop()

if __name__ == '__main__':
    app = App()
    app.mainloop()
