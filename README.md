# TestTaskChatLabs
 aiogram postgresql docker

## Код написан в соответсвии с [Тестовым заданием](https://docs.google.com/document/d/1xqDH_dgCPx71sRElnDQ3Ryns1cUDpAXOiC1vRacEx1g/edit?pli=1)

## Что нужно для запуска?
    - docker  
    - Данные карты для тестовых платежей: 1111 1111 1111 1026 12/22 000
    - создание файла .env в корне проекта c полями:
        BOT_TOKEN=
        POSTGRES_USER=user
        POSTGRES_PASSWORD=
        POSTGRES_DB=database
        POSTGRES_HOST=db
        POSTGRES_PORT=
        U_KASSA_TOKEN=
    !!! В случае изменения полей, уже имеющих значения, придётся так же изменить и docker-compose.yml !!!

## Как запустить?
  Открыть терминал в корне проекта и ввести ```docker-compose up --build -d```

## Функционал бота

_Команды_:

    /start /help - Получить это сообщение и выйти в главное меню

_Главное меню_:

    "Оставить заявку" - Следуя инструкциям бота, вы можете оставить заявку на создание чат-бота для вашего бизнеса
    
    "Купить товар" - Вы можете приобрети 'Условную единицу' за 100₽ или 2 за 200₽
    
    "Мой баланс" - Вы можете посмотреть ваш баланс в у.е.
    
_Админка_:

    "Отправить сообщение пользователям" - Создать рассылку (функции админки видят только администарторы)


