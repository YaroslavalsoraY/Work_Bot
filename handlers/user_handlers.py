from aiogram.filters import CommandStart, StateFilter
from aiogram import Router, F
from aiogram.types import Message, FSInputFile, CallbackQuery
from lexicon.lexicon import LEXICON_RU
from keyboards.keyboard import (start_keyboard,
                                vacancy_keyboard, after_keyboard,
                                create_pagination_kb)
from services.work import FSM_Vacancies, get_vacancies
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from database.database import user_dict_template, users_db
from copy import deepcopy

router = Router()


# Этот хэндлер реагирует на нажатие кнопки "Информация о какансиях"
@router.callback_query(F.data == 'start_button_1')
async def pressed_1(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(LEXICON_RU['question1'])
    await state.set_state(FSM_Vacancies.choosing_vacancy)


# Этот хэндлер принимает ключевое слово для поиска вакансии
@router.message(StateFilter(FSM_Vacancies.choosing_vacancy))
async def vacancy_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_vacancy=message.text.lower())
    await message.answer(
        text=LEXICON_RU['question2'],
        reply_markup=vacancy_keyboard
    )


# Этот хэндлер возвращает пользователя к выбору вакансии
@router.callback_query(F.data == 'no')
async def pressed_no(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(LEXICON_RU['question_alt'])
    await state.set_state(FSM_Vacancies.choosing_vacancy)


# Этот хэндлер выдаёт пользователю найденные вакансии
@router.callback_query(F.data == 'yes',
                       StateFilter(FSM_Vacancies.choosing_vacancy))
async def quantity_chosen(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    users_db[callback.from_user.id]['variants'] =\
        get_vacancies(user_data['chosen_vacancy'])
    if len(users_db[callback.from_user.id]['variants']) > 1:
        await callback.message.answer(
            text=users_db[callback.from_user.id]['variants']
            [users_db[callback.from_user.id]['index']],
            reply_markup=create_pagination_kb(
                'backward',
                f'{users_db[callback.from_user.id]["index"] + 1}/'
                f'{len(users_db[callback.from_user.id]["variants"])}',
                'forward')
            )
    else:
        await callback.message.answer(
            text=users_db[callback.from_user.id]['variants'][0],
            reply_markup=after_keyboard
            )
    await state.set_state(FSM_Vacancies.vacancy_chosen)


# Хэндлер для кнопки "вперёд"
@router.callback_query(F.data == 'forward',)
async def process_forward_press(callback: CallbackQuery):
    if users_db[callback.from_user.id]["index"] + 1 <\
     len(users_db[callback.from_user.id]["variants"]):
        users_db[callback.from_user.id]["index"] += 1
        await callback.message.edit_text(
            text=users_db[callback.from_user.id]['variants']
            [users_db[callback.from_user.id]['index']],
            reply_markup=create_pagination_kb(
                'backward',
                f'{users_db[callback.from_user.id]["index"] + 1}/'
                f'{len(users_db[callback.from_user.id]["variants"])}',
                'forward')
        )
    else:
        users_db[callback.from_user.id]["index"] += 1
        await callback.message.edit_text(
            text=LEXICON_RU['question_aft'],
            reply_markup=create_pagination_kb(
                'backward',
                'button_aft'
            )
        )


# Хэндлер для кнопки "назад"
@router.callback_query(F.data == 'backward')
async def process_backward_press(callback: CallbackQuery):
    if users_db[callback.from_user.id]["index"] > 0:
        users_db[callback.from_user.id]["index"] -= 1
        await callback.message.edit_text(
            text=users_db[callback.from_user.id]['variants']
            [users_db[callback.from_user.id]['index']],
            reply_markup=create_pagination_kb(
                'backward',
                f'{users_db[callback.from_user.id]["index"] + 1}/'
                f'{len(users_db[callback.from_user.id]["variants"])}',
                'forward')
        )
    else:
        await callback.answer()


# Возвращает пользователя в главное меню
@router.callback_query(F.data == 'button_aft')
async def process_start_command_again(callback: CallbackQuery,
                                      state: FSMContext):
    photo = FSInputFile("lexicon\\photo.png")
    users_db[callback.from_user.id] = deepcopy(user_dict_template)
    await callback.message.delete()
    await callback.message.answer_photo(photo,
                                        caption=LEXICON_RU['/start2'],
                                        reply_markup=start_keyboard)
    await state.clear()


# Этот хэндлер реагирует на команду /start
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    photo = FSInputFile("lexicon\\photo.png")
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)
    await message.answer_photo(photo,
                               caption=LEXICON_RU['/start'],
                               reply_markup=start_keyboard)
