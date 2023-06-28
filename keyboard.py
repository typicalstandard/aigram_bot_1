from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message,ReplyKeyboardMarkup)
from aiogram.utils.keyboard import ReplyKeyboardBuilder,InlineKeyboardBuilder
from aiogram import Bot, Dispatcher, types



# Создаем объекты инлайн-кнопок
big_button_1: InlineKeyboardButton = InlineKeyboardButton(
    text='БОЛЬШАЯ КНОПКА 1',
    callback_data='big_button_1_pressed')

big_button_2: InlineKeyboardButton = InlineKeyboardButton(
    text='БОЛЬШАЯ КНОПКА 2',
    callback_data='big_button_2_pressed')

# Создаем объект инлайн-клавиатуры


# Создаем объекты инлайн-кнопок
big_button_3: InlineKeyboardButton = InlineKeyboardButton(
    text='Перевести',
    callback_data='big_button_3_pressed')

big_button_4: InlineKeyboardButton = InlineKeyboardButton( text="Язык по умолчанию",
    callback_data="big_button_4_pressed")

big_button_5: InlineKeyboardButton = InlineKeyboardButton(
    text='Добавить в словарь?',
    callback_data='big_button_5_pressed')


# Создаем объект инлайн-клавиатуры
job: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[big_button_3],
                     [big_button_4],
                     [big_button_5]])

keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[big_button_1],
                     [big_button_2]])




# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data 'big_button_1_pressed' или 'big_button_2_pressed'


