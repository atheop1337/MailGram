from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ChatAction
from modules.libraries.dbms import Database
from modules.languages import en, ru
from modules.libraries.const import _States
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

    async def handle(self, source: Union[types.Message, types.CallbackQuery], state: FSMContext, callback_data: str):
        await self.get_info(source)
        state_name = await state.get_state()

        if isinstance(source, types.Message):
            await self._handle_message(source, state, state_name, callback_data)
        elif isinstance(source, types.CallbackQuery):
            await self._handle_callback_query(source, state, state_name, callback_data)

    async def _handle_message(self, message: types.Message, state: FSMContext, state_name: str, callback_data: str):
        raise NotImplementedError("This method should be implemented by subclasses")

    async def _handle_callback_query(self, callback: types.CallbackQuery, state: FSMContext, state_name: str, callback_data: str):
        raise NotImplementedError("This method should be implemented by subclasses")


class Handlers:
    class StartHandler(BaseHandler):
        async def _handle_message(self, message: types.Message, state: FSMContext, state_name: str, callback_data: str):
            logging.info(f"Handling start message for user {self._user_id}")
            
            exist = await self._db.insert_user(self._user_id, self._username)
            
            if exist == 409:
                user_data = await self._db.fetch_info(self._user_id)
                language = user_data.get("language")
                
                welcome_message = en.Messages_Service.WELCOME_MESSAGE(self._username) if language == "en" else ru.Messages_Service.WELCOME_MESSAGE(self._username)
                
                await message.answer(welcome_message)
            else:
                await message.answer(en.Messages_Service.WELCOME_MESSAGE(self._username))
                
        async def _handle_callback_query(self, callback: types.CallbackQuery, state: FSMContext, state_name: str, callback_data: str):
            logging.info(f"Handling start callback query for user {self._user_id}")           
            user_data = await self._db.fetch_info(self._user_id)
            language = user_data.get("language")
            
            welcome_message = en.Messages_Service.WELCOME_MESSAGE(self._username) if language == "en" else ru.Messages_Service.WELCOME_MESSAGE(self._username)
            
            await callback.message.answer(welcome_message)
            
    class ProfileHandler(BaseHandler):
        async def _handle_message(self, message: types.Message, state: FSMContext, state_name: str, callback_data: str):
            if state_name is None:
                
                if callback_data in (None, "profile"):
                    logging.info(f"Handling profile message for user {self._user_id}")
                    user_data = await self._db.fetch_info(self._user_id)
                    language = user_data.get("language")
                    
                    profile_message = en.Messages_Service.PROFILE_MESSAGE(user_data) if language == "en" else ru.Messages_Service.PROFILE_MESSAGE(user_data)
                    profile_keyboard = en.Buttons_Service.PROFILE_MENU_BUTTONS() if language == "en" else ru.Buttons_Service.PROFILE_MENU_BUTTONS()
                    
                    await message.answer(text=profile_message, reply_markup=profile_keyboard)
                    
                elif callback_data == "change_language":
                    await self._handle_change_language(message)
                    
                elif callback_data == "en" or callback_data == "ru":
                    await self._db.change_info(self._user_id, "language", callback_data)
                    await self._handle_message(message, state, state_name, callback_data = "profile")
                    
                elif callback_data == "change_credentials":
                    await self._handle_change_credentials(message, state)
                    
            elif state_name == _States.ChangeCredentials.new_cred:
                await self._handle_apply_credentials(message, state)
            
        async def _handle_callback_query(self, callback: types.CallbackQuery, state: FSMContext, state_name: str, callback_data: str):
            if state_name is None:
                if callback_data in (None, "profile"):
                    logging.info(f"Handling profile callback query for user {self._user_id}")
                    user_data = await self._db.fetch_info(self._user_id)
                    language = user_data.get("language")
                    
                    profile_message = en.Messages_Service.PROFILE_MESSAGE(user_data) if language == "en" else ru.Messages_Service.PROFILE_MESSAGE(user_data)
                    profile_keyboard = en.Buttons_Service.PROFILE_MENU_BUTTONS() if language == "en" else ru.Buttons_Service.PROFILE_MENU_BUTTONS()
                    
                    await callback.message.answer(text=profile_message, reply_markup=profile_keyboard)
                    
                elif callback_data == "change_language":
                    await self._handle_change_language(callback.message)
                    
                elif callback_data == "en" or callback_data == "ru":
                    await self._db.change_info(self._user_id, "language", callback_data)
                    await self._handle_message(callback.message, state, state_name, callback_data = "profile")
                    
                elif callback_data == "change_credentials":
                    await self._handle_change_credentials(callback.message, state)
                    
            elif state_name == _States.ChangeCredentials.new_cred:
                await self._handle_apply_credentials(callback.message, state)
                
        async def _handle_change_language(self, message: types.Message):
            logging.info(f"Handling change language for user {self._user_id}")
            user_data = await self._db.fetch_info(self._user_id)
            language = user_data.get("language")
            
            if language == "en":
                await message.answer(text = en.Messages_Service.CHANGE_LANGUAGE_MESSAGE(), reply_markup=en.Buttons_Service.LANGUAGE_CHOICE_BUTTONS())
            else:
                await message.answer(text = ru.Messages_Service.CHANGE_LANGUAGE_MESSAGE(), reply_markup=ru.Buttons_Service.LANGUAGE_CHOICE_BUTTONS())
                
        async def _handle_change_credentials(self, message: types.Message, state: FSMContext):
            logging.info(f"Handling change credentials for user {self._user_id}")
            user_data = await self._db.fetch_info(self._user_id)
            language = user_data.get("language")
            await message.answer(text = en.Messages_Service.CHANGE_CREDENTIALS_MESSAGE() if language == "en" else ru.Messages_Service.CHANGE_CREDENTIALS_MESSAGE())
            await state.set_state(_States.ChangeCredentials.new_cred)
            
        async def _handle_apply_credentials(self, message: types.Message, state: FSMContext):
            logging.info(f"Handling apply credentials for user {self._user_id}")
            document = message.document

            if not document:
                logging.error("No document attached.")
                await message.answer("Please send a valid credentials file.")
                return

            try:
                file = await message.bot.get_file(document.file_id)
                file_path = f"tokens\\{self._user_id}_credentials.json"
                await message.bot.download_file(file.file_path, file_path)
                await self._db.change_info(self._user_id, "credentials", file_path)
                await state.clear()
                await message.answer("Your credentials have been updated successfully!")
            except Exception as e:
                logging.error(f"Error downloading file: {e}")
                await message.answer("Failed to download the file. Please try again.")