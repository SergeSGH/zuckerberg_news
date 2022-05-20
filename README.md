# zuckerberg_news
### Описание:
проект социальной сети, с возможностью публиковать собственные новости
а также просматривать избранные новости и ставить оценки

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/SergeSGH/zuckerberg_news.git
```
```
cd zuckerberg_news/infra
```

В папке проекта создать файл .env в котором определить ключевые переменные:
```
DB_ENGINE: вид БД
DB_NAME: имя БД
POSTGRES_USER: логин пользователя БД
POSTGRES_PASSWORD: пароль пользователя БД
DB_HOST: приложение БД 
DB_PORT: порт БД
```

Собрать и запустить контейнеры:
```
docker-compose up -d --build
```

Инициировать БД и перенести в нее данные:
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py loaddata fixtures.json
```