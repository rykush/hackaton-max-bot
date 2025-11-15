from aiomax.router import Router
from aiomax.types import Message
from aiomax.buttons import KeyboardBuilder, MessageButton, LinkButton
from app.handbook.questionPull import pull
import os

router = Router()

@router.on_message()
async def handbook_routing(message: Message):
    if message.body.text in ["Справочник", "справочник", "Guide", "guide", "/guide"]:
        await main_functional(message=message)
    elif message.body.text in pull.keys():
        await question_pull(message=message)
    else:
        thema = None
        for theme in pull.keys():
            if str(message.body.text)[:120] in [quest[:120] for quest in pull[theme]]:
                thema = theme
        if thema:
            await answer(message=message, thema=thema)

async def main_functional(message: Message):
    kb = KeyboardBuilder()
    themes = iter(pull.keys())
    for theme in themes:
        try:
            kb.row(MessageButton(theme), MessageButton(next(themes)))
        except Exception as e:
            print(e)
            kb.row(MessageButton(theme))
    await message.send(f"Выберите направление по которому хотите получить консультацию:\n{'\n'.join(pull.keys())}",
        keyboard=kb)

async def question_pull(message: Message):
    kb = KeyboardBuilder()
    questions = iter(pull[message.body.text].keys())
    for quest in questions:
        try:
            kb.row(MessageButton(str(quest)[:120]), MessageButton(str(next(questions))[:120]))
        except Exception as e:
            kb.row(MessageButton(quest))
    kb.row(MessageButton("Справочник"))
    await message.send(f"Выберите интерисующий Вас вопрос:\n{'\n'.join(pull[message.body.text].keys())}",
        keyboard=kb)

async def answer(message: Message, thema: str):
    answer = pull[thema][[ans for ans in pull[thema] if message.body.text in str(ans)][0]]
    if type(answer) is tuple:
        kb = KeyboardBuilder()
        kb.row(LinkButton("Посмотреть", answer[1]))
        kb.row(MessageButton(thema))
        kb.row(MessageButton("Справочник"))
        await message.send(answer[0], keyboard=kb)
    else:
        kb = KeyboardBuilder()
        kb.row(MessageButton(thema))
        kb.row(MessageButton("Справочник"))
        await message.send(answer, keyboard=kb)