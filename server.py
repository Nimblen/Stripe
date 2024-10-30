from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from task import process_webhook
import stripe
import logging
import config

app = FastAPI()


logger = logging.getLogger("stripe_webhook")
logging.basicConfig(level=logging.INFO)

@app.post("/webhook")
async def stripe_webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature")

    try:
        # Проверяем подлинность запроса от Stripe
        event = stripe.Webhook.construct_event(payload, sig_header, config.STRIPE_WH_TOKEN)
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        logger.error("Ошибка проверки подписи вебхука: %s", str(e))
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Логируем получение вебхука
    logger.info(f"Получен вебхук Stripe: {event['type']}")

    # Отправляем данные вебхука в фоновую задачу Celery для обработки
    background_tasks.add_task(process_webhook.delay, event)

    return {"status": "received"}
