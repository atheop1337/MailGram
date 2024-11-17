from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart, Command
from modules.handlers import start_handler, profile_handler
from modules.libraries.const import _States
from typing import Union

router = Router()

@router.message(CommandStart())
@router.callback_query(F.data == "start")
async def cmd_start_handler(source: Union[types.Message, types.CallbackQuery], state: FSMContext):
    await start_handler.handle(source, state, callback_data="start")
    
@router.message(Command("profile"))
@router.message(_States.ChangeCredentials.new_cred)
@router.callback_query(F.data.in_({"profile", "change_credentials", "change_language", "en", "ru"}))
async def cmd_profile_handler(source: Union[types.Message, types.CallbackQuery], state: FSMContext):
    callback_data = "profile"
    if isinstance(source, types.CallbackQuery):
        callback_data = source.data
    await profile_handler.handle(source, state, callback_data)