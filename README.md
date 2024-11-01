

**Проект Stripe Checkout с FastAPI и Celery**
=============================================

**Описание**
---------------

Этот проект демонстрирует интеграцию Stripe Checkout с FastAPI для генерации ссылок на оплату и обработки вебхуков с использованием Celery и RabbitMQ для выполнения фоновых задач.

**Структура проекта**
----------------------

*   `generate_link.py`: Файл для генерации ссылки на оплату
*   `server.py`: Файл для обработки вебхуков и фоновых задач
*   `requirements.txt`: Файл зависимостей
*   `README.md`: Описание проекта и инструкции

**Предварительные требования**
-----------------------------

*   Python 3.7 или выше
*   Установленный RabbitMQ (он используется как брокер сообщений для Celery)
*   Аккаунт Stripe с активированным API ключом и настройкой вебхуков

**Установка**
--------------

1.  Клонируйте репозиторий:

    ```bash
git clone https://github.com/Nimblen/Stripe.git
cd Stripe
```

2.  Создайте виртуальное окружение и активируйте его:

    ```bash
python3 -m venv venv
source venv/bin/activate  # Для Linux и MacOS
venv\Scripts\activate  # Для Windows
```

3.  Установите зависимости:

    ```bash
pip install -r requirements.txt
```

**Настройка**
--------------

1.  **Stripe API ключи**: Обновите `generate_link.py` и `server.py` с вашим секретным ключом Stripe (`your_secret_stripe_key`) и секретом вебхука (`your_webhook_secret`).
2.  **RabbitMQ**:

    *   Убедитесь, что RabbitMQ установлен и запущен.
    *   На Linux вы можете запустить его командой:

        ```bash
sudo systemctl start rabbitmq-server
```

    *   На MacOS с Homebrew:

        ```bash
brew services start rabbitmq
```

    *   Настройки подключения к RabbitMQ в `server.py` настроены по умолчанию (`amqp://guest:guest@localhost:5672//`), но вы можете изменить их при необходимости.

**Запуск**
------------

1.  **Генерация ссылки на оплату**:

    *   Чтобы создать ссылку на оплату через Stripe Checkout, запустите:

        ```bash
python generate_link.py
```

    *   Это создаст Checkout Session и выведет в консоль ссылку на оплату.

2.  **Запуск FastAPI и Celery для обработки вебхуков**:

    *   Откройте два новых терминала и выполните следующие команды:

        *   **Запуск Celery воркера**:

            ```bash
celery -A server.celery_app worker --loglevel=info
```

        *   **Запуск FastAPI приложения**:

            ```bash
python server.py
```

    *   FastAPI запустится на `http://localhost:8000` и будет готов принимать вебхуки от Stripe.

**Тестирование**
-----------------

1.  **Тестирование генерации ссылки**:

    *   Запустите `generate_link.py`.
    *   Вы получите ссылку на оплату через Stripe Checkout.
    *   Откройте ссылку в браузере, чтобы протестировать процесс оплаты.

2.  **Тестирование вебхуков**:

    *   После завершения оплаты Stripe отправит вебхук на ваш эндпоинт `/webhook`.
    *   Эндпоинт `/webhook` передаст данные в Celery для фоновой обработки.
    *   Проверьте терминал с Celery воркером, чтобы убедиться, что вебхук был обработан.

**Зависимости**
----------------

Все необходимые зависимости указаны в `requirements.txt`:

```text
fastapi
uvicorn
celery
stripe
amqp  # Для подключения к RabbitMQ
```

Установите их с помощью команды:

```bash
pip install -r requirements.txt
```



**Примечания**
----------------

*   **Webhook Secret**: Чтобы защитить ваш вебхук от поддельных запросов, используйте секрет вебхука от Stripe. Вы можете найти его в настройках вебхуков в Stripe Dashboard.
*   **Панель управления RabbitMQ**: Если вам нужна панель управления RabbitMQ, включите её командой:

    ```bash
sudo rabbitmq-plugins enable rabbitmq_management
```

    После этого панель будет доступна по адресу `http://localhost:15672` (по умолчанию логин и пароль: `guest` / `guest`).

