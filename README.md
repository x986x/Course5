Установка: -загрузить репозиторий;

-выполнить pip install -r requirements.txt ;

-указать данные для доступа к базе данных в файле database.ini.
содержимое database.ini:
[postgresql]
host=localhost
user=postgres
password=Ваш пароль
port=5432


Проект для получения информации из hh и внесение данных в таблицы pgAdmin. Если нужны другие компании, их список можно изменить в файле DBManager.py => id_companies. 

Основной скрипт находится (main) и готов к запуску.
 
get_companies_and_vacancies_count()
 — получает список всех компаний и количество вакансий у каждой компании.
 
get_all_vacancies()
 — получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
 
get_avg_salary()
 — получает среднюю зарплату по вакансиям.
 
get_vacancies_with_higher_salary()
 — получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
 
get_vacancies_with_keyword()
 — получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.