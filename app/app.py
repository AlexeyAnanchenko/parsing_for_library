import requests
import psycopg2

from bs4 import BeautifulSoup
from faker import Faker
from datetime import date


url_base = 'https://books.toscrape.com/catalogue/'

# возьмём только книги определённого жанра для сокращения данных
url = url_base + 'category/books/travel_2/index.html'

# создадим объект для создания псевдо-данных
faker = Faker()

# значения для поделючения к БД
db_name = 'postgres_db'
db_user = 'postgres'
db_pass = 'postgres'
db_host = 'localhost'
db_port = '5432'


def get_book_links(url):
    response = requests.get(url)
    parse = BeautifulSoup(response.text, 'html.parser')
    # книги расположены в упорядоченном списке на странице
    ol_elm = parse.find('ol')

    if ol_elm:
        li_elsms = ol_elm.find_all('li')
        links = []

        # получим ссылки на страницы каждой из книг
        for li in li_elsms:
            href = li.find('a').get('href')
            links.append(url_base + href.replace('../../../', ''))

        return links
    else:
        print('Книг нет на странице!')


def get_parse_book_data(links):
    # данные для БД будем хранить в виде списка словарей, где каждый словарь - строка таблицы 
    result = []

    for link in links:
        response = requests.get(link)
        parse = BeautifulSoup(response.text, 'html.parser')
        dict_for_elm = {'title': parse.find('h1').text}
        # данные о книге расположены в строках таблицы на HTML странице
        tr_elms = parse.find_all('tr')

        for el in tr_elms:
            if el.find('th').text == 'UPC':
                dict_for_elm['cipher_book'] = el.find('td').text
            elif el.find('th').text == 'Price (incl. tax)':
                dict_for_elm['price'] = float(el.find('td').text[2:])
            elif el.find('th').text == 'Availability':
                text = el.find('td').text
                i_symb = text.find('(')
                dict_for_elm['count_instances'] = int(text[i_symb + 1: i_symb + 2])
        
        result.append(dict_for_elm)
    return result


def add_fake_data(data_list):
    # придумаем недостающие данные для таблицы "Книга"

    for el in data_list:
        el['year_public'] = faker.random_int(min=1950, max=2023)
        el['volume_pages'] = faker.random_int(min=200, max=800)
        el['publish_house'] = faker.company()

    return data_list


def gen_fake_reader(count):
    # придумаем данные для таблицы "Читатель"
    readers = []

    for i in range(count):
        readers.append({
            'ticket_num': faker.random_number(digits=6),
            'full_name': f'{faker.first_name()} {faker.last_name()}',
            'address_reader': faker.address(),
            'num_phone': faker.phone_number()
        })

    return readers


def gen_fake_book_reader(books_count, readers_count, count_rows):
    # придумаем данные для таблицы "Читатель_Книга"
    readers_books = []

    for i in range(count_rows):
        readers_books.append({
            'reader_id': faker.random_int(min=1, max=readers_count),
            'book_id': faker.random_int(min=1, max=books_count),
            'date_receipt': faker.date_between(
                                start_date=date(2022, 10, 1), end_date=date(2022, 10, 10)
                            ).strftime('%Y-%m-%d'),
            'date_return': faker.date_between(
                                start_date=date(2022, 10, 10), end_date=date(2022, 10, 20)
                            ).strftime('%Y-%m-%d')
        })

    return readers_books


def connection_to_db():
    # подключаемся к БД
    connection = psycopg2.connect(
        host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_pass,
    )
    cursor = connection.cursor()
    return connection, cursor


def load_data(table, data, cursor):
    # для загрузки данных в таблицу БД, нам нужно будет указать её атрибуты
    headers = data[0].keys()
    headers_for_query = ', '.join(headers)

    # параметризированный запрос executemany принимает значения каждой строки в виде кортежа
    values = [tuple(row.values()) for row in data]

    # создём шаблон запроса с учётом неизвестного кол-ва атрибутов на входе
    query = f'INSERT INTO {table} ({headers_for_query}) VALUES ('
    cursor.executemany(
        query + ', '.join(['%s'] * len(headers)) + ');',
        values
    )



if __name__ == '__main__':
    books = add_fake_data(get_parse_book_data(get_book_links(url)))
    readers = gen_fake_reader(4)

    books_readers = gen_fake_book_reader(
        books_count=len(books),
        readers_count=len(readers),
        count_rows=6
    )

    connection, cursor = connection_to_db()
    load_data('public.book', books, cursor)
    load_data('public.reader', readers, cursor)
    load_data('public.reader_book', books_readers, cursor)

    # сохраняем изменения и закрываем соединение
    connection.commit()
    cursor.close()
    connection.close()
    