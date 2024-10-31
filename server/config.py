from celery import Celery
import stripe
from dotenv import load_dotenv
import os

load_dotenv()

# Настройка Stripe
STRIPE_SK_TOKEN = os.getenv("STRIPE_SK_TOKEN")
STRIPE_WH_TOKEN = os.getenv("STRIPE_WH_TOKEN")
stripe.api_key = STRIPE_SK_TOKEN

# Настройка Celery
celery_app = Celery(
    "stripe_webhooks",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND")
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    broker_connection_retry_on_startup=True
)
import server.task