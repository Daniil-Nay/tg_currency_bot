from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

r: Router = Router()


class UserExchangeStates(StatesGroup):
    typing_currency_proccess = State()
    typing_currency_to_get_course_proccess = State()


@r.message(Command('exchange'))
async def exchange_currency_proccess_1(
        message: Message,
        state: FSMContext,
) -> None:
    """
    Отправляет пользователю сообщение с инструкцией по конвертации валют.

    После выполнения этой функции пользователь должен ввести данные для конвертации
    в формате "ВАЛЮТА1 ВАЛЮТА2 СУММА"
    """
    await message.answer(
        text="Введите количество валюты, которую хотите"
             " конвертировать в рубли или наоборот (нецелое значение через точку: "
             "\nПример: "
             "\n<b>EUR RUB 100 </b> - для конвертации евро в рубли"
             "\n<b>RUB EUR 100.00</b> - для конвертации рубли в евро",
        parse_mode='html'
    )
    await state.set_state(UserExchangeStates.typing_currency_proccess)


def is_number(s):
    """
    Проверяет, является ли строка числом (целым или вещественным).
    :param s (str): Строка, которую нужно проверить.
    :return: bool: True, если строка является числом, иначе False.
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


@r.message(UserExchangeStates.typing_currency_proccess)
async def exchange_currency_proccess_2(
        message: Message,
        redis_session,
        state: FSMContext
) -> None:
    """
    Обрабатывает введенные пользователем данные для конвертации валют.
    Проверяет, что введенные данные соответствуют формату "ВАЛЮТА1 ВАЛЮТА2 СУММА",
    где СУММА является числом. Выполняет конвертацию и отправляет результат пользователю.
    :param message (Message): Сообщение от пользователя, содержащее данные для конвертации.
    :param redis_session: Экземпляр RedisClient.
    :param  state (FSMContext): Контекст состояния машины состояний.
    """
    msg_text: list[str] = message.text.split()
    if len(msg_text) == 3 and is_number(msg_text[-1]):
        print(msg_text[0], msg_text[1], msg_text[2])
        text = (f'{msg_text[0]}-{msg_text[1]}: '
                f'{redis_session.get_exchange(msg_text[0], msg_text[1], msg_text[2])}')
        await state.clear()
    else:
        text = ('Неуспешно.\n<b>EUR RUB 100 </b> - для конвертации евро в рубли'
                '\n<b>RUB EUR 100.00</b> - для конвертации рубли в евро')
    await message.answer(
        text=text,
        parse_mode='html'
    )


@r.message(Command('rate'))
async def get_one_rate_proccess_1(
        message: Message,
        state: FSMContext,
) -> None:
    """
    Отправляет пользователю запрос на ввод валюты для получения её курса.
    После выполнения этой функции пользователь должен ввести код валюты, курс которой
    он хочет узнать.
    :param message (Message): Сообщение от пользователя, содержащее команду /rate.
    :param state (FSMContext): Контекст состояния машины состояний.
    """
    await message.answer(
        text=f'Напишите валюту, курс которой хотите узнать.'
             f'\nПример: <b> EUR </b>',
        parse_mode='html',
    )
    await state.set_state(UserExchangeStates.typing_currency_to_get_course_proccess)


@r.message(UserExchangeStates.typing_currency_to_get_course_proccess)
async def get_one_rate_proccess_2(
        message: Message,
        redis_session,
        state: FSMContext,
) -> None:
    """
    Обрабатывает введённый пользователем код валюты и возвращает её курс.
    Проверяет, что введённый код валюты соответствует формату (три заглавные буквы),
    и отправляет пользователю курс этой валюты.
    :param message (Message): Сообщение от пользователя, содержащее код валюты.
    :param redis_session: Экземпляр RedisClient для получения данных валют.
    :param state (FSMContext): Контекст состояния машины состояний.
    """
    msg_text: list[str] = message.text.split()
    if len(msg_text) == 1 and msg_text[0].isalpha():
        text = f"Для {msg_text[0]}: {redis_session.get(msg_text[0])}"
        await state.clear()
    else:
        text = ('Неуспешно.'
                '\n<b>EUR </b> - для получения курса евро в рублях')
    await message.answer(
        text=text,
        parse_mode='html'
    )


@r.message(Command('rates'))
async def get_all_rates(
        message: Message,
        redis_session
) -> None:
    """
    Отправляет пользователю список всех доступных валют и их курсов.
    :param message (Message): Сообщение от пользователя, содержащее команду /rates.
    :param redis_session: Экземпляр RedisClient для получения данных всех валют.
    """
    rates_text = redis_session.get_rates()
    await message.answer(
        text=f'Список всех валют:\n{rates_text}',
        parse_mode='html'
    )