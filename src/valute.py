import requests


def get_valutes_cbr():
    url = "https://www.cbr.ru/scripts/XML_daily.asp"
    response = requests.get(url=url)
    if response.status_code != 200:
        print('Произошла ошибка получения котировок')
    else:
        return response.text
