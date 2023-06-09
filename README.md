# Where to go

Приложение на Django, представляющее собой интерактивную карту Москвы,
на которой отмечены места активного отдыха и досуга с подробными описаниями и комментариями.

<img src="github_img.png" alt="site" style="height: 320px;" />

Пример сайта развернут [здесь](https://daniilit.pythonanywhere.com/).

Так же вы можете войти в [админку](https://daniilit.pythonanywhere.com/admin/):\
Username: `guest`\
Password: `WtG_guest1`\
В данном аккаунте доступны права только на просмотр данных.


## Запуск

Предполагается запуск на python3.

Установите зависимости:

```sh
pip install -r requirements.txt
```

Перед запуском приложения необходимо установить переменные окружения,\
положив их в файл `.env` в корне приложения, или выполнив команды:

```sh
echo DJANGO_SECRET_KEY=<your key> >> .env
echo DEBUG=<True/False> >> .env
echo ALLOWED_HOSTS=<hosts> >> .env
echo INTERNAL_IPS=<hosts> >> .env
```

\* В переменные ALLOWED_HOSTS и INTERNAL_IPS поместите хосты/домены через запятую, например: "127.0.0.1,localhost",
INTERNAL_IPS можно не указывать, если debug-toolbar не используется.

Подготовьте статику для раздачи с сервера:

```sh
./manage.py collectstatic
```

Создайте базу данных SQLite и накатите миграции:

```sh
./manage.py migrate
```

Запустите приложение командой:

```sh
./manage.py runserver
```

Сайт будет доступен по адресу: [http://127.0.0.1:8000/](http://127.0.0.1:8000/).


## Загрузка новых мест в базу данных

Для загрузки данных выполните:

```sh
./manage.py load_place <url>
```

передайте URL к json вида:

```json
{
    "title": "<Название>",
    "imgs": [
        "<URL к изображению>"
    ],
    "description_short": "Короткое описание",
    "description_long": "Подробное описание в формате HTML",
    "coordinates": {
        "lng": "<Долгота>",
        "lat": "<широта>"
    }
}
```

Для обновления данных следует воспользоваться админкой по адресу: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).


## Цели проекта

Код написан в учебных целях — для курса по Python и веб-разработке на сайте [Devman](https://dvmn.org).
