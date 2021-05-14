import requests
import json
import time

from bs4 import BeautifulSoup
from tqdm import tqdm


headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    }
datenow = time.strftime("%d.%m.%Y-%H.%M")


def get_catalog_urls():
    """
    Функция для получения списка ссылок из каталога.
    """

    url = 'https://nav.tn.ru/catalog/'
    query = requests.get(url, headers=headers)

    if query.status_code != 200:
        raise ConnectionError(f'Сервер недоступен, попробуйте позже - статус код {query.status_code}')
    soup = BeautifulSoup(query.text, 'lxml')
    soup_list = soup.find_all('div', class_='b-catalog__el')

    with open('url_catalog.txt', 'w') as file:
        for i in soup_list:
            url_catalog = i.find('a')['href']
            file.write(f'https://nav.tn.ru{url_catalog}?show_all=true\n')


def catalog_item():
    """
    Функция для получения полного списка товаров из каталога.
    Данные складываются в Json с текущей датой.
    """

    print('Прогресс выполнения скрипта')
    with open('url_catalog.txt') as file:
        lines = [line.strip() for line in file.readlines()]

        for line in tqdm(lines):
            quary = requests.get(line, headers=headers).content
            soup = BeautifulSoup(quary, 'lxml')
            items = soup.find_all('div', class_='b-products__item')

            data_items = []
            data_items.append(soup.find('h1').text)

            for item in items:
                item_title = item.find('div', class_='b-products__title').find('a').text
                item_link = item.find('div', class_='b-products__title').find('a')['href']
                item_description = item.find('div', class_='b-products__text').text.strip()

                data = {
                    'title': item_title,
                    'link': f'https://nav.tn.ru{item_link}',
                    'description': item_description
                }
                data_items.append(data)

            with open(f'data{datenow}.json', 'a', encoding='utf-8') as json_file:
                json.dump(data_items, json_file, indent=4, ensure_ascii=False)


def main():
    get_catalog_urls()
    catalog_item()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Quit')