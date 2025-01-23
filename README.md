# Тестовый проект для конкурса на вакансию middle Python backend-разработчик

## Оглавление

- Инструкция по запуску проекта
- Описание
- Структура проекта
- Кол-во затраченного времени

### Инструкция по запуску проекта

Сначала запустить команду docker-compose build, затем docker-compose up

### Описание

<strong>Задание выполняется для ООО “Строй дом”, компания TOPECOM, руководитель Крайнев Александр Юрьевич.</strong>

Проект состоит, как и указано в ТЗ, из API на фреймворке FastAPI и web-сервера Node js.

Бэкенд реализует модели Users и Roles. Поддерживает получение, добавление, изменение и удаление данных. Все данные хранятся на локальной базе данных SQLite, также используется ORM SQLAlchemy, который гармонично сочетается с FastAPI и Pydantic.

Фронтенд же внешне состоит из одной страницы с двумя таблицами с пользователями и ролями. Он реализует практически все операции API, позволяя просматривать пользователей, создавать новых, редактировать пользователей и удалять их. работает на Vue.js, используя компоненты PrimeVue.

Сначала планировалось разрабатывать проект точно по времени, но после разработки бэкенда выяснилось, что опыта во фронте мне сильно не хватает.

Фронтенд представляет из себя отредактированный шаблон [SAKAI Vue](https://sakai.primevue.org/). При этом шаблон работает на чистом Vite сервере, чтобы разобраться как перенести его на Nuxt js требовалось ещё время, а я и так потратил его на функционал, который, возможно, излишне наворочен. Поэтому фронтенд в итоге работает на Vite.

### Структура проекта

- back - API проекта (Python, FastAPI, SQLAlchemy)
    - main - стартовая точка API
    - schemas - модели для данных, получаемых и выдаваемых API
    - db - реализация компонентов для работы с базой данных
    - roles & users
        - model - модель для базы данных
        - views - реализация работы запросов для взаимодействия с моделями
- front - одностраничный фронтенд web-сервер (Node, Vite, Vue, PrimeVue, axios)
    - src - Содержит основной код для работы приложения
        - main.js - стартовая точка web-сервера
        - App.vue - базовый класс приложения
        - layout/AppLayout.vue - схема страницы
        - components
            - Roles.vue & Users.vue - таблицы с элементами управления для основных операций с соответствующими моделями
        - service
            - Service.vue - класс, реализующий работу с моделями данных через API
            - Utils.vue - необходимые функции
        - assets - набор файлов стилей для работы шаблона с SAKAI
    - index.html - точка входа для фреймворка

### Кол-во затраченного времени

- Создание бэкенда - 5 часов
- Написание фронтенда - 7 часов
- Разбор проблем с интеграцией в Docker - 1-2 часа