from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ChatAction
from modules.libraries.dbms import Database
from modules.languages import en, ru
from typing import Union
import logging


class BaseHandler:
    def __init__(self):
        self._db = Database()
        self._user_id = None
        self._username = None

    async def get_info(self, source: Union[types.Message, types.CallbackQuery]):
        if isinstance(source, (types.Message, types.CallbackQuery)):
            self._user_id = source.from_user.id
            self._username = source.from_user.username

    async def handle(self, source: Union[types.Message, types.CallbackQuery], state: FSMContext):
        await self.get_info(source)
        state_name = await state.get_state()

        if isinstance(source, types.Message):
            await self._handle_message(source, state, state_name)
        elif isinstance(source, types.CallbackQuery):
            await self._handle_callback_query(source, state, state_name)

    async def _handle_message(self, message: types.Message, state: FSMContext, state_name: str):
        raise NotImplementedError("This method should be implemented by subclasses")

    async def _handle_callback_query(self, callback: types.CallbackQuery, state: FSMContext, state_name: str):
        raise NotImplementedError("This method should be implemented by subclasses")


class Handlers:
    class StartHandler(BaseHandler):
        async def _handle_message(self, message: types.Message, state: FSMContext, state_name: str):
            logging.info(f"Handling start message for user {self._user_id}")
            
            exist = await self._db.insert_user(self._user_id, self._username)
            
            if exist == 409:
                user_data = await self._db.fetch_info(self._user_id)
                language = user_data.get("language")
                
                welcome_message = en.Messages_Service.WELCOME_MESSAGE(self._username) if language == "en" else ru.Messages_Service.WELCOME_MESSAGE(self._username)
                
                await message.answer(welcome_message)
            else:
                await message.answer(en.EN_WELCOME_MESSAGE(self._username))
                
        async def _handle_callback_query(self, callback: types.CallbackQuery, state: FSMContext, state_name: str):
            logging.info(f"Handling start callback query for user {self._user_id}")           
            user_data = await self._db.fetch_info(self._user_id)
            language = user_data.get("language")
            
            welcome_message = en.Messages_Service.WELCOME_MESSAGE(self._username) if language == "en" else ru.Messages_Service.WELCOME_MESSAGE(self._username)
            
            await callback.message.answer(welcome_message)
            
    class ProfileHandler(BaseHandler):
        async def _handle_message(self, message: types.Message, state: FSMContext, state_name: str):
            logging.info(f"Handling profile message for user {self._user_id}")
            user_data = await self._db.fetch_info(self._user_id)
            language = user_data.get("language")
            
            profile_message = en.Messages_Service.PROFILE_MESSAGE(user_data) if language == "en" else ru.Messages_Service.PROFILE_MESSAGE(user_data)
            profile_keyboard = en.Buttons_Service.PROFILE_MENU_BUTTONS() if language == "en" else ru.Buttons_Service.PROFILE_MENU_BUTTONS()
            
            await message.answer(text=profile_message, reply_markup=profile_keyboard)
            
        async def _handle_callback_query(self, callback: types.CallbackQuery, state: FSMContext, state_name: str):
            logging.info(f"Handling profile callback query for user {self._user_id}")
            user_data = await self._db.fetch_info(self._user_id)
            language = user_data.get("language")
            
            profile_message = en.Messages_Service.PROFILE_MESSAGE(user_data) if language == "en" else ru.Messages_Service.PROFILE_MESSAGE(user_data)
            profile_keyboard = en.Buttons_Service.PROFILE_MENU_BUTTONS() if language == "en" else ru.Buttons_Service.PROFILE_MENU_BUTTONS()
            
            await callback.message.answer(text=profile_message, reply_markup=profile_keyboard)