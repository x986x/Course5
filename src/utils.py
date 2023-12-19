import requests  # Для запросов по API


def get_info(id_companies):
    """Получаем информацию о компаниях и формируем ее в словарь"""
    company_vacanci = []
    try:
        for id_company in id_companies:
            url_hh = f'https://api.hh.ru/employers/{id_company}'
            info = requests.get(url_hh).json()
            company_vacanci.append({'company_id': info['id'],
                                    'company_name': info['name'],
                                    'description': info['description'],
                                    'url': info['vacancies_url']
                                    })
    except KeyError:
        print("По данным кретериям не нашлось вакансий")
    return company_vacanci


def get_vacanci(url):
    """Получаем информацию о вакансиях, используя url от компании.
            Полученную информацию формируем в словарь"""
    info_vacanci = []
    info = requests.get(url).json()['items']
    salary_max = 0
    try:
        for vacanci in info:
            if vacanci['salary']:
                salary_from = vacanci['salary']['from'] if vacanci['salary']['from'] else 0
                salary_to = vacanci['salary']['to'] if vacanci['salary']['to'] else 0
                salary_avr = (salary_from + salary_to) / 2
                if salary_from > salary_max:
                    salary_max = salary_from
                elif salary_to > salary_max:
                    salary_max = salary_to
            else:
                salary_from = 0
                salary_to = 0
                salary_avr = 0
                salary_max = 0
            info_vacanci.append({'id_vacanci': vacanci['id'],
                                 'id_company': vacanci['employer']['id'],
                                 'name': vacanci['name'],
                                 'url': vacanci['area']['url'],
                                 'salary_from': salary_from,
                                 'salary_to': salary_to,
                                 'salary_avr': salary_avr,
                                 'salary_max': salary_max,
                                 'area': vacanci['area']['name']
                                 })
    except KeyError:
        print("Неправильные критерии поиска")
    return info_vacanci


def delete_symbol(text):
    """Метод для удаления ненужных символов в тексте"""
    symbols = ['\n', '<strong>', '</strong>', '</p>', '<p>',
               '<b>', '</b>', '<ul>', '<br />', '</ul>', '&nbsp', '</li>', '</ul>',
               '&laquo', '&ndash', '&mdash', '<em>', '&middot', '</em>', '&raquo']
    for symbol in symbols:
        text = text.replace(symbol, '')
    return text
