from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

r: Router = Router()


# Основная команда при запуске бота. Возвращает информацию о боте
@r.message(Command('start'))
async def welcoming_handler(
        message: Message
) -> None:
    """
    Хэндлер, который ловит апдейты по первому запуску бота/команде start
    :param message: Текстовое сообщение, получаемое от пользователя
    :return: None
    """

    await message.answer(
        text="<b>Данный бот является программной реализацией ТЗ."
             "</b> Чтобы проверить доступные команды, используйте:\n"
             "/help",
        parse_mode='html',
    )

#Команда для вывода информации о других командах в рамках реализации ТЗ.
@r.message(Command('help'))
async def help_handler(
        message: Message
) -> None:
    """
    Хэндлер, который ловит апдейты по команде help
    :param message: Текстовое сообщение, получаемое от пользователя
    :return: None
    """
    help_text = (
        "Доступные команды:\n"
        "/start - Начальная команда.\n"
        "/exchange - для конвертации валюты (1 команда тз)\n"
        "/rate - узнать курс конкретной валюты (доп команда)\n"
        "/rates - получить список всех валют (2 команда тз)"
    )

    await message.answer(
        text=help_text,
        parse_mode='html'
    )