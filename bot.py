
import asyncio
from aiogram import Bot
from aiogram import Dispatcher
from config.configurations import load_config
from database.redis_client_class import RedisClient

from database.redis_interaction_funcs import update_currency
from handlers import main_handlers, db_intercation_handlers
from middleware import InjectMiddleware


async def main():
    """
    главная функция по запуску бота, инициализации роутеров и миддлвари
    :return:
    """
    config = load_config()
    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher()

    redis_client = RedisClient(host=config.db.redis_host, port=config.db.redis_port)
    redis_client.connect()
    await update_currency(redis_client)
    db_intercation_handlers.r.message.middleware.register(InjectMiddleware(redis_session = redis_client))
    dp.include_routers(main_handlers.r, db_intercation_handlers.r)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
