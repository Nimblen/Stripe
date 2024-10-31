import stripe 
from server import config



def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],   # Типы методов оплаты
            line_items=[
                {
                    'price_data': {
                        'currency': 'USD',
                        'product_data': {
                            'name': 'Оплата услуги',
                            'description': 'Оплата услуги',
                        },
                        'unit_amount': 6000,  # Сумма в центах (например, $60.00)
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',  # Одноразовая оплата
            metadata={        # Дополнительные данные для идентификации
                'sender': 'message.chat.id',
                'connectorID': 1,
                'customerID': 1,
                'employeeID': 1,
                'label': 'dev',
                'invoice_payload': 'Некая строка'
            },
            success_url='https://t.me/yourbot',  # URL успешного платежа
            cancel_url='https://t.me/yourbot',  # URL при отмене
        )
        # Возвращаем URL сессии
        return session.url
    except Exception as e:
        print(f"Ошибка при создании сессии оплаты: {e}")
        return None

# Вызов функции для генерации ссылки
checkout_url = create_checkout_session()
print(f"Ссылка для оплаты: {checkout_url}")