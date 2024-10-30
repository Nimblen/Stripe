from config import celery_app
import logging

logger = logging.getLogger(__name__)

@celery_app.task
def process_webhook(event_data):
    """
    Обрабатывает данные Stripe вебхука в фоне.
    """
    event_type = event_data.get("type")
    metadata = event_data.get("data", {}).get("object", {}).get("metadata", {})

    user_id = metadata.get("user_id")
    order_id = metadata.get("order_id")

    if event_type == "payment_intent.succeeded":
        logger.info(f"Платеж для пользователя {user_id} и заказа {order_id} успешно завершен.")
        # Здесь можно добавить код для обновления статуса заказа в базе данных
    else:
        logger.warning(f"Получен необработанный тип события: {event_type}")

    # Логируем всю полезную информацию
    logger.info(f"Обработано событие: {event_data}")
