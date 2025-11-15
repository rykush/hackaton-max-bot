from aiomax.router import Router
from aiomax.fsm import FSMStorage, FSMCursor
from aiomax.types import Message, Callback
from aiomax.buttons import KeyboardBuilder, MessageButton, LinkButton, CallbackButton
from aiomax.filters import state
from app.platforms.data import data
import random

router = Router()

@router.on_message('База площадок')
async def platforms(message: Message):
    text = f'''Федеральный площадки:
        1. Федеральный портал проектов НПА (уровень Правительства РФ)
        2. Государственная Дума
        3. Центральный Банк
        4. Евразийская экономическая комиссия
    '''
    kb = KeyboardBuilder()
    kb.row(LinkButton('1. Федеральный портал проектов НПА', url='https://regulation.gov.ru/'))
    kb.row(
        LinkButton('2. Государственная Дума', url='https://sozd.duma.gov.ru/'),
        LinkButton('3. Центральный Банк', url='https://cbr.ru/project_na/')
        )
    kb.row(LinkButton('4. Евразийская экономическая комиссия', url='https://eec.eaeunion.org/'))
    kb.row(MessageButton('Региональные площадки'))
    await message.send(text=text, keyboard=kb)

@router.on_message('Региональные площадки')
async def select_regional_platforms(message:Message, cursor: FSMCursor):
    await message.send('Напишите название региона/области\nНапример: \nСвердловская область\nЧувашская Республика - Чувашия')
    cursor.change_state('select_region')
    cursor.change_data({'region': message.content})

@router.on_message(state('select_region'))
async def region_platforms(message: Message, cursor: FSMCursor):
    region = str(message.body.text)
    if region in data.keys():
        kb = KeyboardBuilder()
        if type(data[region]) == str:
            kb.row(LinkButton(region, url=data[region]))
        elif type(data[region]) == list:
            idx = 1
            for url in data[region]:
                kb.row(LinkButton(f'Площадка: {idx}', url=url))
                idx += 1
        text = f'Площадки региона: {region}'
        await message.send(text=text, keyboard=kb)
        cursor.clear()
    else:
        primer = '\n'.join(random.sample(list(data.keys()), min(5, len(data))))
        kb = KeyboardBuilder()
        kb.row(CallbackButton('Отмена', 'cancel'))
        await message.send(text=f'''
                Региона не определён системой.
                Проверьте написание региона и попробуйте ещё раз. 
                Примеры правильного написания регионов:\n {primer}
            ''', keyboard=kb)

@router.on_button_callback(lambda data: data.payload == 'cancel')
async def cancel(cb: Callback, cursor: FSMCursor):
    await cb.message.delete()
    cursor.clear()