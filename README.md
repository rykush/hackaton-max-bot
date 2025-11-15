Для запуска проекта нам потребуется Python версии 3.12.10.

VScode
1) Качаем проект и разархивируем его, запускаем его с помощью VScode, открываем новый терминал и пишем python -m venv venv для загрузки виртуальной среды.
2) Переходим в виртуальную среду прописывая в терминале venv/scripts/activate
3) Качаем зависимости вводя в терминал python -m pip install -r requirements.txt или pip install -r requirements.txt
4) После полной установки прописываем в терминал python app.py
Бот запущен.

Docker
1) Качаем docker с официального сайта и открываем его
2) В терминале VScode прописываем docker-compose up -d , у нас автоматически загрузятся все зависимости и запустится бот

Docker образ
1) Качаем также docker с оф. сайта, открываем его
2) Качаем образ docker pull rykush/hakaton-bot:latest
3) Запускаем командой docker run -d

## Токен бота отправится отдельно от проекта, его нужно будет вставить в файл config.py, который находится в корневой папке проекта, TOKEN = "СЮДА ТОКЕН"

# Установленные библиотеки проекта
- **aiofiles==25.1.0**
- **aiohappyeyeballs==2.6.1**
- **aiohttp==3.13.2**
- **aiomax==2.12.2**
- **aiosignal==1.4.0**
- **alembic==1.17.1**
- **APScheduler==3.11.1**
- **attrs==25.4.0**
- **beautifulsoup4==4.14.2**
- **bs4==0.0.2**
- **certifi==2025.10.5**
- **charset-normalizer==3.4.4**
- **frozenlist==1.8.0**
- **greenlet==3.2.4**
- **idna==3.11**
- **Mako==1.3.10**
- **MarkupSafe==3.0.3**
- **multidict==6.7.0**
- **pip==25.0.1**
- **propcache==0.4.1**
- **requests==2.32.5**
- **soupsieve==2.8**
- **SQLAlchemy==2.0.44**
- **typing_extensions==4.15.0**
- **tzdata==2025.2**
- **tzlocal==5.3.1**
- **urllib3==2.5.0**
- **yarl==1.22.0**
