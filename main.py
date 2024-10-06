import requests
from lxml import html
import csv


# Обработка получаемых данных
def check_val(val):
    if len(val) != 0:
        res = val[0].strip()
    else:
        res = None
    return res


# URL сайта с табличными данными
url = 'https://calcus.ru/strany'

# Установка заголовков, чтобы имитировать браузер
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
}

# Отправка HTTP GET-запроса
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Проверка на ошибки HTTP
except requests.exceptions.RequestException as e:
    print(f'Ошибка при запросе к сайту: {e}')
else:
    # Парсинг HTML содержимого
    tree = html.fromstring(response.content)

    # Извлечение данных таблицы с использованием XPath
    try:
        data = []
        # Заполняем заголовки столбцов
        columns = tree.xpath('//table/thead/tr[1]/th/text()')
        data.append([col.strip() for col in columns])
        
        rows = tree.xpath('//table/tbody/tr')  # Путь к строкам таблицы

        for row in rows:
            country_name = row.xpath(".//td//div[contains(@class, 'fw-bold')]/text()")[0].strip()
            capital = check_val(row.xpath('.//td[2]/text()'))
            iso_codes = check_val(row.xpath(".//td[3]/text()"))
            telephone_code = check_val(row.xpath(".//td[4]/text()"))
            currency = check_val(row.xpath(".//td[5]/text()"))
        
            data.append([country_name, capital, iso_codes, telephone_code, currency])  

    except Exception as e:
        print(f'Ошибка при извлечении данных: {e}')
    else:
        # Сохранение данных в CSV-файл
        with open('countries_data.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(data)  # Запись данных

        print('Данные успешно сохранены в countries_data.csv')
