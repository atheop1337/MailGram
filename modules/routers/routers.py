from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart, Command
from modules.handlers import start_handler, profile_handler
from typing import Union

router = Router()

@router.message(CommandStart())
async def cmd_start_handler(source: Union[types.Message, types.CallbackQuery], state: FSMContext):
    await start_handler.handle(source, state)
    
@router.message(Command("profile"))
@router.callback_query(F.data == "profile")
async def cmd_profile_handler(source: Union[types.Message, types.CallbackQuery], state: FSMContext):
    await profile_handler.handle(source, state)