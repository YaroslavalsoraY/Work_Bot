from aiogram.filters import CommandStart
from aiogram import Router, F
from aiogram.types import Message, FSInputFile, CallbackQuery
from lexicon.lexicon import LEXICON_RU
from keyboards.keyboard import (start_keyboard,
                                vacancy_keyboard, after_keyboard)
from services.work import Find_vacancies, get_vacancies
from aiogram.fsm.context import FSMContext
import time

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
    for i in get_vacancies(user_data['chosen_vacancy'], 20):
        time.sleep(1.5)
        await callback.message.answer(text=i)
    state.clear()
    await callback.message.answer(
        text=LEXICON_RU['question_aft'],
        reply_markup=after_keyboard
        )


@router.callback_query(F.data == 'start')
async def process_start_command_again(callback: CallbackQuery):
    photo = FSInputFile("lexicon\\photo.png")
    await callback.message.answer_photo(photo,
                                        caption=LEXICON_RU['/start2'],
                                        reply_markup=start_keyboard)


@router.message(CommandStart())
async def process_start_command(message: Message):
    photo = FSInputFile("lexicon\\photo.png")
    await message.answer_photo(photo,
                               caption=LEXICON_RU['/start'],
                               reply_markup=start_keyboard)

# @router.callback_query(F.data == 'start_button_2')
# async def pressed_2(callback: CallbackQuery):
#     await callback.answer('2', show_alert=True)
