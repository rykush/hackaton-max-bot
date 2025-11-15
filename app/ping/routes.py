from aiomax.router import Router
from aiomax.types import Message, Callback
from aiomax.buttons import KeyboardBuilder, MessageButton, CallbackButton
from app.database.session import get_db
from app.database.models import User_setting
import os

router = Router()

@router.on_message('Уведомления')
async def start_ping(message: Message):
    db = next(get_db())
    user = db.query(User_setting).filter_by(max_id=message.user_id).first()
    if user is None:
        kb = KeyboardBuilder()
        kb.add(CallbackButton('Принять', 'successful_maxid'))
        await message.send(f'''
            Для отправки уведомлений по фильтрам, мне необходимо разрешение на хранения Вашего MAX_ID.
            MAX_ID необходим для сохранения выбранных Вами фильтров.
            Нажмите кнопку ниже если согласны с хранением Вашего MAX_ID в боте.
            ''',
            keyboard=kb)
    else:
        kb = KeyboardBuilder()
        # kb.row(CallbackButton('Настройки', 'settings'))
        if user.on_off:
            kb.row(CallbackButton('Отключить', 'disable'))
        else:
            kb.row(CallbackButton('Активировать', 'activate'))
        await message.send(
            text= 'Уведомления включены' if user.on_off else 'Уведомления выключены', 
            keyboard=kb
            )

@router.on_button_callback(lambda data: data.payload == 'successful_maxid')
async def successful_maxid(cb: Callback):
    db = next(get_db())
    if db.query(User_setting).filter_by(max_id=cb.user_id).first() is None:
        user = User_setting(
            max_id=cb.user_id
        )
        db.add(user)
        db.commit()
    kb = KeyboardBuilder()
    # kb.row(CallbackButton('Настройки', 'settings'))
    kb.row(CallbackButton('Включить', 'activate'))
    await cb.message.edit(
        text= 'Уведомления включены' if user.on_off else 'Уведомления выключены', 
        keyboard=kb
        )

@router.on_button_callback(lambda data: data.payload == 'activate')
async def ping_activate(cb: Callback):
    db = next(get_db())
    user = db.query(User_setting).filter_by(max_id=cb.user_id).first()
    user.on_off = True
    db.commit()
    kb = KeyboardBuilder()
    kb.row(CallbackButton('Отключить', 'disable'))
    await cb.message.edit(text='Уведомления включены', keyboard=kb)

@router.on_button_callback(lambda data: data.payload == 'disable')
async def ping_disable(cb: Callback):
    db = next(get_db())
    user = db.query(User_setting).filter_by(max_id=cb.user_id).first()
    user.on_off = False
    db.commit()
    kb = KeyboardBuilder()
    kb.row(CallbackButton('Активировать', 'activate'))
    await cb.message.edit(text='Уведомления выключены', keyboard=kb)
