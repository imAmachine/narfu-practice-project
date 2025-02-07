# Сервис по выбору общежития САФУ

Этот проект разрабатывается в образовательных целях. Основная цель проекта состоит в следующем:

- Просмотр списка общежитий.
- Отправка заявок на проживание в общежитии в университет.
- Упрощение процесса рассмотрения заявок администрацией университета.

## Описание

Этот проект разрабатывается для обеспечения удобного и простого выбора общежития для студентов САФУ. Студенты могут просмотреть список доступных общежитий, отправить заявку на проживание и рассмотрение ее администрацией университета. Проект предоставляет удобный и эффективный способ оформления заявок и упрощает процесс поиска подходящего общежития для студентов.

## Инструкция по установке

1. Клонируйте репозиторий на вашу локальную машину:

git clone https://github.com/imAmachine/narfu-practice-project.git


2. Перейдите в каталог проекта:

cd your-repository


3. Установите зависимости, указанные в файле requirements.txt:

pip install -r requirements.txt

4. Восстановите базу данных из приложенного бэкапа db_backup (PostgreSQL)

5. Отредактируйте файл connection.json для настройки подключения к базе данных. Укажите необходимые параметры подключения (например, имя пользователя, пароль, хост и имя базы данных).

6. Запустите приложение:

python app.py

Приложение будет запущено на локальном сервере по адресу http://localhost:5000.

## Технологии

Этот проект был разработан с использованием следующих технологий:

- Flask Framework
- Python
- HTML
- CSS
- JavaScript

## Благодарности

Хочу выразить благодарность пользователю "GuerdySSS" за помощь в разработке FrontEnd части проекта.

Ведущий разработчик: "imAmachine"
