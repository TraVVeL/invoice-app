import sqlite3

# Создание соединения с базой данных
conn = sqlite3.connect('facture.db')

# Создание объекта-курсора
cursor = conn.cursor()

# Создание таблицы в базе данных
cursor.execute('''CREATE TABLE IF NOT EXISTS facture (
                inn TEXT, 
                current_date TEXT, 
                full_name TEXT, 
                code TEXT, 
                amount TEXT, 
                price TEXT, 
                excise TEXT, 
                tax TEXT,
                signature TEXT, 
                contract_number TEXT, 
                inn_buyer TEXT, 
                sender TEXT,
                buyer TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS user_data (
                name TEXT, 
                surname TEXT, 
                card TEXT, 
                date_exp TEXT, 
                card_cvv TEXT, 
                email TEXT
                )''')


# Сохранение изменений и закрытие базы данных
conn.commit()
