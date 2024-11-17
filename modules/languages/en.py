from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class Messages_Service:
    
    @staticmethod
    def WELCOME_MESSAGE(username: str) -> str:
        return f"Pleasure to see you, {username}!"
    
    @staticmethod
    def PROFILE_MESSAGE(userdata: dict) -> str:
        return f"🔑 ID: {userdata.get('user_id')}\n😃 Name: {userdata.get('username')}\n🕘 Registered: {userdata.get('created_at')}\n✨ Language: {userdata.get('language')}\n🕶 Credentials: {userdata.get('credentials')}."


class Buttons_Service:
    
    @staticmethod
    def PROFILE_MENU_BUTTONS() -> InlineKeyboardMarkup:
        kb = [
            [InlineKeyboardButton(text="🕶 Change credentials", callback_data = "change_credentials")],
            [InlineKeyboardButton(text="✨ Change language", callback_data = "change_language")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=kb)