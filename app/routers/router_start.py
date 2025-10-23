from aiogram import Router, F, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from app.keyboards import keyboards
from app.databases.db_handler import UserDatabase
router = Router()

@router.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    keyboard = keyboards.start_kb()

    async with UserDatabase("app/databases/users.db") as db:
        await db.add_elem(message.from_user.id, message.from_user.first_name, message.from_user.username, 0)

    await message.answer("Привет! Я - бот от ССО #1!" \
    " \nНажми \"Выбрать комнату\", чтобы посмотреть свободное время для этой комнаты." \
    " \nНажми \"Помощь\", чтобы посмотреть список доступных команд.", reply_markup=keyboard)

@router.message(F.text == "Помощь")
async def help(message: types.Message):
    keyboard = keyboards.start_kb()
    await message.answer("Нихуя я тебе не помогу иди нахуй", reply_markup=keyboard)

@router.message(Command("_stud"))
async def chmod(message: types.Message):
    keyboard = keyboards.start_kb()
    async with UserDatabase("app/databases/users.db") as db:
        await db.chmod(message.from_user.id)
    await message.answer("Статус изменен!", reply_markup=keyboard)

