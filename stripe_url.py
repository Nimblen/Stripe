import stripe 
import config



def create_checkout_session():
    try:
        # Создание Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],   # Типы методов оплаты, например, только карта
            line_items=[                     # Товары для оплаты
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Товар или услуга',  # Название товара
                        },
                        'unit_amount': 2000,  # Сумма в центах (например, $20.00)
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',                   # Режим "payment" для одноразовой оплаты
            success_url='https://t.me/bot_username',  # URL для успешного платежа
            cancel_url='https://t.me/bot_username',  # URL при отмене оплаты
        )
        # Возвращаем URL сессии
        return session.url
    except Exception as e:
        print(f"Ошибка при создании сессии оплаты: {e}")
        return None

# Вызов функции
checkout_url = create_checkout_session()
print(f"Ссылка для оплаты: {checkout_url}")
