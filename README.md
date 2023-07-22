# parsing_for_library
Задание на парсинг данных и заполнения ими таблиц Базы данных "Библиотеки"

В рамках задания реализовано мини-приложение в docker-compose, которое состоит из 2-х контейнеров:
1. БД "Библиотека" в PostgreSQL, в котором автоматически в контейнере создаются 3 таблицы: "Книги", "Читатели", "Книги_Читатели"
2. Парсер на Python, который:
    - парсит сайт с продажей книг и забирает данные подходящие для заливки в таблицу "Книги" с помощью библиотеки beautifulsoup4
    - недостающую информацию заполняет псевдо-данными с помощью библиотеки faker
    - остальные 2 таблицы полностью заполняются псевдо-данными с помощью faker
    - как итог, данные отправляются в БД через бибилиотеку для работы PostgreSQL из Python - psycopg2

## Из чего состоит проект?

- Скрипт DDL для создания таблиц: <code>[./db_data/DDL/init.sql](https://github.com/AlexeyAnanchenko/parsing_for_library/blob/main/db_data/DDL/init.sql)</code>.
- ER-диаграмма БД: <code>[./db_data/ER_diagram.png](https://github.com/AlexeyAnanchenko/parsing_for_library/blob/main/db_data/ER_diagram.png)</code>.
- Скрипт для парсинга сайта: <code>[./parser/parser.py](https://github.com/AlexeyAnanchenko/parsing_for_library/blob/main/parser/parser.py)</code>.
- Dockerfile для создания образа: <code>[./parser/Dockerfile](https://github.com/AlexeyAnanchenko/parsing_for_library/blob/main/parser/Dockerfile)</code>.
- Скриншоты залитых данных в БД после отработки парсера: <code>[./screenshots/](https://github.com/AlexeyAnanchenko/parsing_for_library/blob/main/screenshots/)</code>.
-  docker-compose.yml для разворачивания проекта: <code>[./docker-compose.yml](https://github.com/AlexeyAnanchenko/parsing_for_library/blob/main/docker-compose.yml)</code>.

## Как развернуть проект?

Для просмотра проекта достаточно склонировать его себе на локальный компьютер, иметь установленным docker-compose и ввести команду:

```sh
docker-compose up -d
```

Далее база данных доступна в контейнере, либо по порту 5432 из любого сервиса для подключения к БД (например, DBeaver)