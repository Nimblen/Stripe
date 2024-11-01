import stripe

# Настройки Stripe API с секретным ключом
stripe.api_key = ""  # Укажите ваш секретный ключ Stripe

def create_checkout_session(
    amount=6000, 
    currency="USD", 
    success_url="https://t.me/yourbot", 
    cancel_url="https://t.me/yourbot",
    sender="default_sender",
    connectorID=1,
    customerID=1,
    employeeID=1,
    label="dev",
    invoice_payload="Некая строка"
):
    """
    Создает ссылку на сессию Stripe Checkout с возможностью указания различных параметров.
    
    Параметры:
    - amount: int - Сумма в центах.
    - currency: str - Валюта.
    - success_url: str - URL для перенаправления при успешной оплате.
    - cancel_url: str - URL для перенаправления при отмене оплаты.
    - sender: str - Идентификатор отправителя (метаданные).
    - connectorID: int - Идентификатор соединителя (метаданные).
    - customerID: int - Идентификатор клиента (метаданные).
    - employeeID: int - Идентификатор сотрудника (метаданные).
    - label: str - Метка (метаданные).
    - invoice_payload: str - Дополнительная информация о платеже (метаданные).
    """
    try:
        # Создание сессии Stripe Checkout
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],  
            line_items=[
                {
                    'price_data': {
                        'currency': currency,
                        'product_data': {
                            'name': 'Оплата услуги',
                            'description': 'Оплата услуги',
                        },
                        'unit_amount': amount,  # Сумма в центах
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',  # Одноразовая оплата
            metadata={  # Дополнительные данные для идентификации
                'sender': sender,
                'connectorID': connectorID,
                'customerID': customerID,
                'employeeID': employeeID,
                'label': label,
                'invoice_payload': invoice_payload
            },
            success_url=success_url,  # URL при успешной оплате
            cancel_url=cancel_url,   # URL при отмене
        )
        # Возвращаем URL сессии для оплаты
        return session.url
    except Exception as e:
        print(f"Ошибка при создании сессии оплаты: {e}")
        return None

# Вызов функции для генерации ссылки с указанием аргументов
if __name__ == "__main__":
    # Здесь можно передать любые аргументы
    checkout_url = create_checkout_session(
        amount=5000,  # Сумма в центах, например, $50.00
        sender="new_sender",
        connectorID=2,
        customerID=5,
        employeeID=3,
        label="production",
        invoice_payload="Тестовая строка"
    )
    if checkout_url:
        print(f"Ссылка для оплаты: {checkout_url}")
