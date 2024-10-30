from celery import Celery
import stripe
from dotenv import load_dotenv
import os


load_dotenv()

STRIPE_SK_TOKEN = os.getenv("STRIPE_SK_TOKEN")
STRIPE_WH_TOKEN = os.getenv("STRIPE_WH_TOKEN")
stripe.api_key = STRIPE_SK_TOKEN


celery_app = Celery(
    "stripe_webhooks",
    broker="redis://localhost:6379/0", 
    backend="redis://localhost:6379/1"
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
