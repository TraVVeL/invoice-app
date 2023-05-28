import datetime
import re


class Validator:
    def __init__(self):
        pass

    @staticmethod
    def is_inn_kpp(inn_kpp):
        if not inn_kpp:
            return False

        # Разделяем ИНН и КПП
        try:
            inn, kpp = inn_kpp.split('/')
        except ValueError:
            return False

        # Проверяем ИНН
        if not inn.isdigit() or len(inn) not in (10, 12):
            return False
        if len(inn) == 10:
            coefficients = [2, 4, 10, 3, 5, 9, 4, 6, 8]
            control_sum = sum(int(coefficient) * int(digit) for coefficient, digit in zip(coefficients, inn)) % 11
            if control_sum > 9:
                control_sum = 0
            if control_sum != int(inn[-1]):
                return False
        else:
            coefficients1 = [7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
            coefficients2 = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
            control_sum1 = sum(
                int(coefficient) * int(digit) for coefficient, digit in zip(coefficients1, inn[:10])) % 11
            control_sum2 = sum(
                int(coefficient) * int(digit) for coefficient, digit in zip(coefficients2, inn[:11])) % 11
            if control_sum1 > 9:
                control_sum1 = 0
            if control_sum2 > 9:
                control_sum2 = 0
            if control_sum1 != int(inn[-2]) or control_sum2 != int(inn[-1]):
                return False

        # Проверяем КПП
        if not kpp.isdigit() or len(kpp) != 9:
            return False

        return True

    @staticmethod
    def is_date(date_str):
        try:
            date = datetime.datetime.strptime(date_str, '%d.%m.%Y')
            if date.date() < datetime.datetime.today().date():
                return False
            else:
                return True
        except ValueError:
            return False

    @staticmethod
    def is_fullname(full_name):
        """
        Проверяет, что введенное ФИО состоит из трех слов, где каждое слово начинается с заглавной буквы.
        Возвращает True, если ФИО корректное, и False в противном случае.
        """
        fio_parts = full_name.split()
        if len(fio_parts) != 3:
            return False
        for part in fio_parts:
            if not part.isalpha():
                return False
        return True

    @staticmethod
    def is_number(input_string):
        try:
            return input_string.isdigit()
        except ValueError:
            return False

    @staticmethod
    def is_in_range(input_string):
        if input_string in range(1, 1_000_000):
            return True
        return False

    @staticmethod
    def is_percent(string):
        # Удаляем все пробелы из строки
        string = string.replace(" ", "")

        # Проверяем, заканчивается ли строка на символ %
        if string.endswith("%"):
            # Если да, то удаляем символ % и проверяем, состоит ли оставшаяся часть строки только из цифр
            return string[:-1].isdigit()
        else:
            return False

    @staticmethod
    def is_name(name: str) -> bool:
        """
        Функция проверяет, является ли ввод именем на латинице.
        Возвращает True, если все символы в слове являются буквами латинского алфавита,
        и False в противном случае.
        """
        if len(name) < 2:
            return False

        return all(c.isalpha() and c.isascii() for c in name)

    @staticmethod
    def is_valid_credit_card_number(cc_number):
        """
        Проверяет, является ли переданный номер кредитной карты действительным
        :param cc_number: str, номер кредитной карты
        :return: bool, True если номер действительный, False в противном случае
        """

        # Избавляемся от всех нецифровых символов и переводим номер в строку
        cc_number = str(cc_number).replace(' ', '').replace('-', '')

        # Проверяем, что номер содержит только цифры
        if not cc_number.isdigit():
            return False

        # Проверяем, что номер состоит из 13, 15 или 16 цифр
        if not (len(cc_number) == 13 or len(cc_number) == 15 or len(cc_number) == 16):
            return False

        # Вычисляем контрольную сумму по алгоритму Луна
        sum_dig = 0
        num_digits = len(cc_number)
        oddeven = num_digits & 1
        for i in range(0, num_digits):
            digit = int(cc_number[i])

            if not ((i & 1) ^ oddeven):
                digit *= 2

            if digit > 9:
                digit -= 9

            sum_dig += digit

        return (sum_dig % 10) == 0

    @staticmethod
    def is_valid_credit_card_date(expiration_date):
        """
        Проверяет, является ли переданная дата действительной для использования
        в качестве даты истечения срока действия кредитной карты
        :param expiration_date: str, дата истечения срока действия кредитной карты в формате "ММ/ГГ"
        :return: bool, True если дата действительна, False в противном случае
        """

        # Разбиваем строку даты на месяц и год
        try:
            exp_month, exp_year = expiration_date.split('/')
        except ValueError:
            return False

        # Проверяем, что месяц и год состоят из цифр
        if not (exp_month.isdigit() and exp_year.isdigit()):
            return False

        # Преобразуем месяц и год в числа
        exp_month = int(exp_month)
        exp_year = int(exp_year)

        # Проверяем, что месяц и год находятся в нужном диапазоне
        if not (1 <= exp_month <= 12 and datetime.datetime.now().year <= exp_year <= datetime.datetime.now().year + 10):
            return False

        # Все хорошо
        return True

    @staticmethod
    def is_valid_cvv(cvv):
        """
        Проверяет, является ли переданный CVV-код действительным
        :param cvv: str, CVV-код
        :return: bool, True если код действительный, False в противном случае
        """

        # Проверяем, что код состоит из 3 или 4 цифр
        if not (len(cvv) == 3 or len(cvv) == 4):
            return False

        # Проверяем, что код содержит только цифры
        if not cvv.isdigit():
            return False

        # Все хорошо
        return True

    @staticmethod
    def is_valid_email(email):
        """
        Проверяет, является ли переданный email действительным
        :param email: str, email-адрес
        :return: bool, True если email действительный, False в противном случае
        """

        # Проверяем, что email соответствует формату адреса электронной почты
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match(pattern, email):
            return False

        # Все хорошо
        return True
