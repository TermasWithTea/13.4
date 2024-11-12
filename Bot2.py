import logging
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram import Router
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import asyncio

logging.basicConfig(level = logging.DEBUG)

api = '7843730721:AAHprrD38Ilc5vPwKLQ94bsaCpB-ctCeJ7A'
bot = Bot(token = api)
storage = MemoryStorage()
dp = Dispatcher(storage=MemoryStorage())
router = Router()


class UserState(StatesGroup):
    name = State()
    age = State()
    growth = State()
    weight = State()


    @router.message(Command('start'))
    async def start_massage(message: types.Message, state:FSMContext):
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=[
            [
             types.KeyboardButton(text = 'Результат'),
             types.KeyboardButton(text = 'Информация'),
            ]
        ],
            resize_keyboard= True)
        await message.answer('Добро Пожаловать в калькулятор калорий! Выберите кнопку:', reply_markup=keyboard)
        await state.update_data(start=message.text)

        user_data = await state.get_data()
        await state.set_state(UserState.name)

    @router.message(lambda message: message.text.lower() == 'результат')
    async def set_age(message: types.Message, state:FSMContext):
        await message.reply(f'Введите свой возраст:')
        await state.set_state(UserState.age)

    @router.message(age)
    async def set_growth(message:types.Message, state:FSMContext):
        await state.update_data(age = message.text)
        user_data = await state.get_data()
        await message.reply('Введите свой рост:')
        await state.set_state(UserState.growth)

    @router.message(growth)
    async def set_weight(message: types.Message, state:FSMContext):
        await state.update_data(growth = message.text)
        user_data = await state.set_state()
        await message.reply('Введите свой вес:')
        await state.set_state(UserState.weight)

    @router.message(weight)
    async def set_calories(message: types.Message, state:FSMContext):
        await state.update_data(weight = message.text)
        data = await state.get_data()
        age = int(data.get('age'))
        growth = int(data.get('growth'))
        weight = int(data.get('weight'))
        user_data = await state.get_data()
        bmr = 10 * weight + 6.25 * growth - 5 * age + 5

        daily_calories = bmr * 1.2

        await message.answer(f'Ваша норма калорий:{daily_calories:.2f} ккал.')
        await state.clear()



dp.include_router(router)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())


