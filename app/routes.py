from aiomax import BotStartPayload
from aiomax.router import Router
from aiomax.types import Message
from aiomax.buttons import KeyboardBuilder, MessageButton


router = Router()

@router.on_bot_start()
async def on_bot_start(payload: BotStartPayload):
    kb = KeyboardBuilder()
    kb.row(MessageButton("База площадок"))
    kb.row(MessageButton("Уведомления"))
    kb.row(MessageButton("Справочник"))
    await payload.send(
        '''Вас приветствует цифровой помощник в мире публичных консультаций. 
        Я экономлю ваше время, отправляя персональные уведомления о новых и резонансных проектах, отвечаю на вопросы по процедурам и помогаю сориентироваться в площадках для обсуждений. 
        Чем могу помочь?''', 
        keyboard=kb)