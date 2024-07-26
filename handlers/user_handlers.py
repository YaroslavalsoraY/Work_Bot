from aiogram.filters import CommandStart
from aiogram import Router, F
from aiogram.types import Message, FSInputFile, CallbackQuery
from lexicon.lexicon import LEXICON_RU
from keyboards.keyboard import (start_keyboard,
                                vacancy_keyboard, after_keyboard,
                                create_pagination_kb)
from services.work import Find_vacancies, get_vacancies
from aiogram.fsm.context import FSMContext
from database.database import user_dict_template, users_db
from copy import deepcopy

router = Router()


@router.callback_query(F.data == 'start_button_1')
async def pressed_1(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(LEXICON_RU['question1'])
    await state.set_state(Find_vacancies.choosing_vacancy)


@router.message(Find_vacancies.choosing_vacancy)
async def vacancy_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_vacancy=message.text.lower())
    await message.answer(
        text=LEXICON_RU['question2'],
        reply_markup=vacancy_keyboard
    )
    await state.set_state(Find_vacancies.choosing_quantity)


@router.callback_query(F.data == 'no')
async def pressed_no(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(LEXICON_RU['question_alt'])
    await state.set_state(Find_vacancies.choosing_vacancy)


@router.callback_query(F.data == 'yes')
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


@router.callback_query(F.data == 'forward')
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


@router.callback_query(F.data == 'button_aft')
async def process_start_command_again(callback: CallbackQuery):
    photo = FSInputFile("lexicon\\photo.png")
    users_db[callback.from_user.id] = deepcopy(user_dict_template)
    await callback.message.answer_photo(photo,
                                        caption=LEXICON_RU['/start2'],
                                        reply_markup=start_keyboard)


@router.message(CommandStart())
async def process_start_command(message: Message):
    photo = FSInputFile("lexicon\\photo.png")
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)
    await message.answer_photo(photo,
                               caption=LEXICON_RU['/start'],
                               reply_markup=start_keyboard)
