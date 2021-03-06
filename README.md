# Yatube

## Описание проекта
Это социальная сеть для публикации личных дневников.
Можно создать свою страницу. Если на нее зайти, то можно посмотреть все записи автора. Пользователи могут заходить на чужие страницы, подписываться на авторов и комментировать их записи. Модерирование записей и блокирование пользователей через Админ панель. Записи можно отправить в сообщество и посмотреть там записи разных авторов.

## Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:

```
https://github.com/meferyliv/yatube.git
```

```
cd yatube
```

Cоздать и активировать виртуальное окружение:
```
python3 -m venv venv
```

```
source venv/bin/activate
```

Обновить менеджер пакетов pip и установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip  
```

```
pip install -r requirements.txt
```

Выполнить миграции и запустить проект:
```
python3 manage.py migrate
```

```
python3 manage.py runserver
```
