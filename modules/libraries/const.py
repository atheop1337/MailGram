from aiogram.fsm.state import State, StatesGroup

class _States:
    
    class ChangeLanguage(StatesGroup):
        new_lang = State()