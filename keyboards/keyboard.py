from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicon.lexicon import LEXICON_RU

start_button_1 = InlineKeyboardButton(
    text=LEXICON_RU['start_button_1'],
    callback_data='start_button_1'
)

start_button_2 = InlineKeyboardButton(
    text=LEXICON_RU['start_button_2'],
    callback_data='start_button_2'
)

start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[start_button_1],
                     [start_button_2]]
)


vacancy_yes = InlineKeyboardButton(text=LEXICON_RU['yes'], callback_data='yes')
vacancy_no = InlineKeyboardButton(text=LEXICON_RU['no'], callback_data='no')

vacancy_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[vacancy_yes],
                     [vacancy_no]]
)

after_button = InlineKeyboardButton(
    text=LEXICON_RU['button_aft'],
    callback_data='start'
)

after_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[after_button]]
)
