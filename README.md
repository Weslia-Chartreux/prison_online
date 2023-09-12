# prison_online

## Описание

Телеграмм бот, который оценивает сообщения пользователей на предмет нарушения закона на основе gpt. Ничего серьёзного в боте не заложено, т.к. gpt склонен ошибаться и нести чушь.
Но как развлечение в беседе друзей сойдет). 

## Использование в телеграмм

Для работы нужно добавить бота в беседу и выдать права на просмотр сообщений(это делается в BotFather). При вводе команды /prison_online анализирует N последних сообщений, которые бот видел и еще не анализировал.
Если бот не получил команду на анализ, но новые N сообщений появились, то бот без команды сам анализирует. Переменная N находится в app/src/bot/handlers.py под именем SEND_GPT_MESSAGE (дефолтное значение 50)

## Сборка

1. Переменные окружения, которые нужны: токен тг и токен chatgpt. Они описаны в docker-compose. Можно запускать свой .env, добавив --env-file config/config.env и убрав лишние строчки из compose.

2. В файле app/src/chat_modes.yml описаны основная "косметика" бота.
   
     1) gpt_mode - выбираем какие версии gpt использовать ("gpt-3.5-turbo-16k", "gpt-3.5-turbo", "gpt-4). Рекомендую всё-таки gpt-4
     2) message_start и message_finish отвечают за сообщения, которые пишет до и после статей бот.
     3) prompt_start - основной промпт проекта (если будете пытаться его изменять, то осторожнее с отловом сообщений gpt, в которых он не уверен в нарушениях)

3. 🔥 Запуск проекта:
    ```bash
    docker-compose up --build
    ```
