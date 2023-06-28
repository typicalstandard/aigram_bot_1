import logging
import pycld2 as cld2
from geopy.geocoders import Nominatim
from aiogram.filters import Command, CommandStart, StateFilter
from  aiogram.filters import Text
from  environs import Env
from aiogram.filters import Command, CommandStart
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.redis import RedisStorage, Redis
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from keyboard import job,keyboard
from aiogram.methods.send_location import SendLocation
import db
from aiogram import F
import json
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message,KeyboardButton)
env = Env()              # Создаем экземпляр класса Env
env.read_env()


import translators as translator

### usage
 # Optional. Caching sessions in advance, which can help improve access speed.



logging.basicConfig(level=logging.INFO)

redis: Redis = Redis(host='localhost')

# Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
storage: RedisStorage = RedisStorage(redis=redis)

bot = Bot(token=env('API_TOKEN'))

# For example use simple MemoryStorage for Dispatcher.
dp = Dispatcher(storage=storage)




class Form(StatesGroup):
    text = State()  # Will be represented in storage as 'Form:name'
    translation = State()
    location = State()
    language_1 = State()
    language_2 = State() # Will be represented in storage as 'Form:age'
    word = State()

import random

async  def on_startup(_):
    await  db.get_all_products()
    print('подключение к БД')




@dp.message(Command(commands='db'))
async def cmd_start(message: types.Message):
    await message.answer('Словарь',reply_markup=keyboard)


@dp.callback_query(Text(text='big_button_1_pressed'))
async  def  cb_get_all_product(callback: types.CallbackQuery):
     products = await db.get_all_products()
     if not products:
         await callback.message.answer('НЕТ')
     else:
            await callback.message.answer(products)



@dp.callback_query(Text(text='big_button_2_pressed'))
async  def cb_add_new_product(callback:types.CallbackQuery,state: FSMContext)-> None:
    await callback.message.answer('Добавляй')
    await state.set_state(Form.word)





@dp.message(Command(commands='trans'))
async def user_regis(message: types.Message):
    await message.answer('Переводчик',reply_markup= job)

@dp.callback_query(Text(text='big_button_4_pressed'))
async  def language(callback:types.CallbackQuery,state: FSMContext):
        await state.set_state(Form.location)
        builder = ReplyKeyboardBuilder()
        builder.add(
            types.KeyboardButton(text="Запросить геолокацию", request_location=True))
        await callback.message.answer(text = 'ru',reply_markup=builder.as_markup(resize_keyboard=True))
@dp.message(StateFilter(Form.location))
async def get_username(message: types.Message, state: FSMContext):
    geolocator = Nominatim(user_agent="domen")
    location = geolocator.reverse(f"{message.location.latitude}, {message.location.longitude}")
    print(list(location.address.split(',')[-1]))

@dp.callback_query(Text(text='big_button_3_pressed'))
async  def language(callback:types.CallbackQuery,state: FSMContext):
    await callback.answer('Напишите текст')
    await state.set_state(Form.text)
@dp.message(StateFilter(Form.text))
async def get_username(message: types.Message, state: FSMContext,word = 'ru'):
    await state.update_data(text=message.text)
    data = await state.get_data()
    if cld2.detect(data['text'])[0] == True and cld2.detect(data['text'])[2][0][1] != word:
            await message.answer(translator.translate_text(data['text'], from_language= cld2.detect(data['text'])[2][0][1], to_language=word, translator='alibaba'))
    else:
        await message.answer(text = "Выберите язык текста")
        await state.set_state(Form.language_1)

@dp.message(StateFilter(Form.language_1))
async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(language_1=message.text)
    await state.set_state(Form.language_2)
    await message.answer(text="На какой?")


@dp.message(StateFilter(Form.language_2))
async def get_address(message: types.Message, state: FSMContext):
        await state.update_data(language_2=message.text)
        data = await state.get_data()
        await message.answer(translator.translate_text(data['text'], from_language= data['language_1'] , to_language=data['language_2'] , translator='alibaba'))

        await state.clear()


@dp.callback_query(Text(text='big_button_5_pressed'))
async  def language(callback:types.CallbackQuery,state: FSMContext):
    await callback.answer('Язык по умолчанию "ru" ')

if __name__ == "__main__":
    dp.run_polling(bot,
                   dispatcher=dp,
                   skip_updates=True,
                   on_startup=on_startup)

