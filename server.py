from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from celery import Celery
import stripe

# Настройки API ключа Stripe и конфигурация Celery
SECRET_KEY = ""
WH_SECRET_KEY = ""
stripe.api_key = SECRET_KEY

app = FastAPI()

# Настройка Celery с использованием RabbitMQ как брокера
celery_app = Celery(
    "tasks",
    broker="amqp://guest:guest@localhost:5672//",  # Подключение к RabbitMQ
    backend="rpc://"
)

# Функция обработки вебхука от Stripe
@celery_app.task
def process_webhook(event_data):
    event_type = event_data.get("type")
    metadata = event_data.get("data", {}).get("object", {}).get("metadata", {})

    user_id = metadata.get("sender")
    connector_id = metadata.get("connectorID")
    customer_id = metadata.get("customerID")
    employee_id = metadata.get("employeeID")
    label = metadata.get("label")
    invoice_payload = metadata.get("invoice_payload")

    if event_type == "checkout.session.completed":
        print(f"Платеж успешно завершен для: {user_id}, {connector_id}, {customer_id}, {employee_id}, {label}, {invoice_payload}")
    else:
        print(f"Получен необработанный тип события: {event_type}")

    print(f"Обработано событие: {event_data}")

# Эндпоинт для обработки вебхуков от Stripe
@app.post("/webhook")
async def stripe_webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature")

    try:
        # Проверка подлинности вебхука от Stripe
        event = stripe.Webhook.construct_event(payload, sig_header, WH_SECRET_KEY)
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        print(f"Ошибка проверки подписи вебхука: {e}")
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Логирование типа события
    print(f"Получен вебхук Stripe: {event['type']}")

    # Добавляем задачу в Celery для фоновой обработки
    background_tasks.add_task(process_webhook, event)

    return {"status": "received"}

# Запуск приложения FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
