from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class Messages_Service:
    
    @staticmethod
    def WELCOME_MESSAGE(username: str) -> str:
        return f"Добро пожаловать, {username}!"
    
    @staticmethod
    def PROFILE_MESSAGE(userdata: dict) -> str:
        return f"🔑 ID: {userdata.get('user_id')}\n😃 Имя: {userdata.get('username')}\n🕘 Зарегистрирован: {userdata.get('created_at')}\n✨ Язык: {userdata.get('language')}\n🕶 Credentials: {userdata.get('credentials')}."

    @staticmethod
    def CHANGE_LANGUAGE_MESSAGE() -> str:
        return "Выберите язык: "

class Buttons_Service:
    
    @staticmethod
    def PROFILE_MENU_BUTTONS() -> InlineKeyboardMarkup:
        kb = [
            [InlineKeyboardButton(text="🕶 Изменить credentials", callback_data = "change_credentials")],
            [InlineKeyboardButton(text="✨ Изменить язык", callback_data = "change_language")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=kb)
    
    @staticmethod
    def LANGUAGE_CHOICE_BUTTONS() -> InlineKeyboardMarkup:
        kb = [
            [InlineKeyboardButton(text="🇺🇸 English", callback_data = "en"), InlineKeyboardButton(text="🇷🇺 Русский", callback_data = "ru")],
        ]
        return InlineKeyboardMarkup(inline_keyboard=kb)
        