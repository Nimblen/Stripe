from server.config import celery_app
import logging

logger = logging.getLogger(__name__)

@celery_app.task(name="server.task.process_webhook")
def process_webhook(event_data):
    event_type = event_data.get("type")
    metadata = event_data.get("data", {}).get("object", {}).get("metadata", {})

    user_id = metadata.get("user_id")
    order_id = metadata.get("order_id")

    if event_type == "payment_intent.succeeded":
        logger.info(f"Платеж для пользователя {user_id} и заказа {order_id} успешно завершен.")
        # Добавьте обработку этого события
    elif event_type == "checkout.session.completed":
        logger.info("Обработка checkout.session.completed")
        # Добавьте код для обработки события checkout.session.completed
    else:
        logger.warning(f"Получен необработанный тип события: {event_type}")

    logger.info(f"Обработано событие: {event_data}")

