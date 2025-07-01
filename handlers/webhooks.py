from handlers.payments import PaymentHandler


async def ckassa_webhook(request, bot, storage):
    data = await request.json()
    handler = PaymentHandler(bot, storage)
    return await handler.handle(data)
