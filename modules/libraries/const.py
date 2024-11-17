from aiogram.fsm.state import State, StatesGroup

class _States:
    
    class ChangeCredentials(StatesGroup):
        new_cred = State()