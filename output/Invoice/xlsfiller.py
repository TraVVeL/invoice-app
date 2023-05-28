# -*- coding: utf-8 -*-
"""
Created : 08.05.2023

@author: --
"""


from docxtpl import DocxTemplate
from uuid import uuid4
from datetime import datetime
import os
import smtp

current_dir = os.path.abspath(os.getcwd())

print(current_dir)


def gen_id():
    return uuid4()


set_id = gen_id()


class XlsFiller:
    def __int__(self):
        self.generate_id = uuid4()

    def get_filename(self):
        file_name = f"{set_id}.docx"
        return file_name

    def get_email(self):
        return ...

    def call_event_to_fill_the_blank(self, USER_BILL, USER_MAIL):
        print(USER_MAIL)
        months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля',
                  'августа', 'сентября', 'октября', 'ноября', 'декабрь']
        doc = DocxTemplate(f"{current_dir}\\invoice_instance.docx")

        day, month, year = datetime.today().day, months[datetime.today().month - 1], datetime.today().year
        BILL = {
            'CORRECTION': "--",
            'DATE_FROM1': f"{day} {month} {year}",
            'DATE_FROM2': "--",

            'SELLER': "ООО \"Любушкина мечта\" ",
            'CARGO_SENDER': "--",
            'ADDRESS_1': "118000, г.Москва, ул. Ленина, д475, оф.34",
            'ADDRESS_2': "118000, г.Москва, ул. Маркса, д.98, оф 139",
            'SIGNATURE_2': "Дуткина",
            'FULL_NAME_2': "Дуткина И.Р",

            'ROW_COLUMN_0_0': "Аренда торгового павильона по договору №94 от 07.01.2016 г. за сентябрь 2016г."
        }
        BILL.update(USER_BILL)

        RC_05 = BILL.get('ROW_COLUMN_0_5')
        RC_06 = BILL.get('ROW_COLUMN_0_6')
        RC_07 = BILL.get('ROW_COLUMN_0_7')

        RC_08 = int(RC_05) * int(RC_06.replace('%', '')) / 100
        RC_09 = int(RC_05) + RC_08
        RC_3_4 = int(RC_05) + RC_08
        BILL_CALC = {
            'ROW_COLUMN_0_8': RC_08,
            'ROW_COLUMN_0_9': RC_09,
            'ROW_COLUMN_3_4': RC_3_4
        }
        BILL.update(BILL_CALC)
        doc.render(BILL)
        file = f"{current_dir}\\{self.get_filename()}"

        doc.save(f"{current_dir}\\{self.get_filename()}")
        smtp.send_email_with_attachment('danilmiheev38@gmail.com',
                                        'pbnyegfwxzuhmfgu',
                                        USER_MAIL,
                                        'Счёт-фактура',
                                        'Ваш счёт-фактура',
                                        f"{current_dir}\\{self.get_filename()}")
