from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
import re
from datetime import datetime

from app.keyboards import keyboards

router = Router()

available_rooms = ['626']

def is_date_valid(date):
    format_pattern = r'^\d{2}-\d{2}-\d{4}$'
    if not re.match(format_pattern, date):
        return False
    try:
        date_obj = datetime.strptime(date, '%d-%m-%Y')
        return True
    except ValueError as e:
        return False
    
def is_time_valid(interval_str):
    strict_pattern = r'^([01][0-9]|2[0-3]):([0-5][0-9])-([01][0-9]|2[0-3]):([0-5][0-9])$'
    match = re.match(strict_pattern, interval_str)
    if not match:
        return False
    
    start_h, start_m, end_h, end_m = match.groups()
    
    start_total = int(start_h) * 60 + int(start_m)
    end_total = int(end_h) * 60 + int(end_m)
    
    if start_total >= end_total:
        return False
    
    return True

# states group for fsm
class Booking(StatesGroup):
    choosing_room = State()
    choosing_date = State()
    choosing_time = State()

@router.message(F.text.lower() == 'выбрать комнату')
async def choose_room(message: Message, state: FSMContext):
    keyboard = keyboards.rooms_kb()
    await message.answer('Выберите комнату: ', reply_markup=keyboard)
    await state.set_state(Booking.choosing_room)

@router.message(Booking.choosing_room, F.text.in_(available_rooms))
async def choose_date(message: Message, state: FSMContext):
    await state.update_data(chosen_room = message.text.lower())
    await message.answer('Отлично! Теперь выберите дату. Формат - дд-мм-гггг. ', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Booking.choosing_date)

@router.message(Booking.choosing_date)
async def choose_time(message: Message, state: FSMContext):
    if is_date_valid(message.text):
        await state.update_data(chosen_date = message.text.lower())
        await message.answer('Осталось только выбрать время! Формат - чч:мм-чч:мм.')
        await state.set_state(Booking.choosing_time)
    else:
        await message.answer('Неверный формат даты!')

@router.message(Booking.choosing_time)
async def book(message: Message, state: FSMContext):
    keyboard = keyboards.start_kb()
    if is_time_valid(message.text):
        await state.update_data(chosen_time = message.text.lower())
        await message.answer('Комната забронирована! На этом моменте отправляется лог в студ', reply_markup=keyboard)
        await state.clear()
    else:
        await message.answer('Неверный формат времени!')