import psycopg2
from utils import get_info, get_vacanci, delete_symbol
from confing import config

id_companies = [1740,  # яндекс
                2222,  # цемрос
                78638,  # тинькоф
                15478,  # vk
                4181,  # ВТБ
                333,  # Consort
                3529,  # сбер
                84585,  # Авито
                1272486,  # Сбермаркет
                1375441]  # Okko


class DBManager:
    def __init__(self, db_name, params):
        self.db_name = db_name  # название базы данных
        self.params = params  # параметры подключение, получаем через config

    def connect_db(self):
        """Метод для подключения и создания БЗ"""

        connection = psycopg2.connect(database='postgres', **self.params)
        connection.autocommit = True
        cursor = connection.cursor()
        try:
            cursor.execute(f"DROP DATABASE IF EXISTS {self.db_name}")
            cursor.execute(f"CREATE DATABASE   {self.db_name}")
        except psycopg2.ProgrammingError:
            pass

        cursor.close()
        connection.close()

    def create_table(self):
        """Метод для создания таблиц с компаниями и вакансиями"""

        connection = psycopg2.connect(database=self.db_name, **self.params)
        with connection.cursor() as cursor:
            try:
                cursor.execute("""
                           CREATE TABLE companies (
                           company_id int PRIMARY KEY,
                           company_name varchar(50) NOT NULL,
                           description text
                           )
                           """)

                cursor.execute("""
                            CREATE TABLE vacanci (
                            id_vacanci int PRIMARY KEY,
                            company_id int REFERENCES companies(company_id) NOT NULL,
                            vacanci_name varchar(100) NOT NULL,
                            url varchar(100) NOT NULL,
                            salary_from varchar(100), 
                            salary_to varchar(100),
                            salary_avr varchar(100),
                            salary_max varchar(100),
                            aria varchar(100)
                            )
                            """)

            except psycopg2.ProgrammingError:
                print("Таблицы не созданы")
        connection.commit()
        connection.close()

    def write_info_in_table(self):
        """Метод для заполнения информацией таблиц компаний и вакансий.
              Используются функции get_info, get_vacanci"""

        connection = psycopg2.connect(database=self.db_name, **self.params)
        hh = get_info(id_companies)
        with connection.cursor() as cursor:
            for i in range(len(hh)):
                hh_replace = delete_symbol(hh[i]['description'])  # удаляем ненужные символы из текста
                hh_gv = get_vacanci(hh[i]['url'])
                cursor.execute("""INSERT INTO companies VALUES (%s,%s,%s)""",
                               (hh[i]['company_id'], hh[i]['company_name'], hh_replace))
                for count in range(len(hh_gv)):
                    cursor.execute("""INSERT INTO vacanci VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s )""",
                                   (hh_gv[count]['id_vacanci'], hh_gv[count]['id_company'],
                                    hh_gv[count]['name'], hh_gv[count]['url'],
                                    hh_gv[count]['salary_from'], hh_gv[count]['salary_to'],
                                    hh_gv[count]['salary_avr'], hh_gv[count]['salary_max'],
                                    hh_gv[count]['area'],
                                    ))

        connection.commit()
        connection.close()

    def get_companies_and_vacancies_count(self):
        connection = psycopg2.connect(database=self.db_name, **self.params)
        with connection.cursor() as cursor:
            cursor.execute("""SELECT company_name, COUNT(vacanci_name) AS count_vacancies 
                                FROM companies
                                JOIN vacanci USING (company_id) 
                                GROUP BY companies.company_id """)
            rows = cursor.fetchall()
            for row in rows:
                print(row)

        connection.commit()
        connection.close()

    def get_all_vacancies(self):
        connection = psycopg2.connect(database=self.db_name, **self.params)
        with connection.cursor() as cursor:
            cursor.execute("""SELECT companies.company_name, vacanci.vacanci_name, 
                                vacanci.salary_avr, vacanci.url 
                                FROM companies
                                JOIN vacanci USING (company_id) """)
            rows = cursor.fetchall()
            for row in rows:
                print(row)

        connection.commit()
        connection.close()

    def get_vacancies_with_higher_salary(self):
        connection = psycopg2.connect(database=self.db_name, **self.params)
        with connection.cursor() as cursor:
            cursor.execute("""SELECT * from vacanci
                              WHERE salary_max > salary_avr
                               ORDER BY salary_max """)
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        connection.commit()
        connection.close()

    def avr_salary(self):
        connection = psycopg2.connect(database=self.db_name, **self.params)
        with connection.cursor() as cursor:
            cursor.execute("""SELECT vacanci_name,salary_avr
                                from vacanci 
                                ORDER BY salary_avr DESC """)
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            connection.commit()
            connection.close()

    def get_vacancies_with_keyword(self, word):
        connection = psycopg2.connect(database=self.db_name, **self.params)
        with connection.cursor() as cursor:
            cursor.execute(f""" SELECT * from vacanci
                              WHERE vacanci_name like '%{word}'
                              OR vacanci_name like '{word}%'
                              OR vacanci_name like '%{word}%' """)
            rows = cursor.fetchall()
            for row in rows:
                print(row)

        connection.commit()
        connection.close()
