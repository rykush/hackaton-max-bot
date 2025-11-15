from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.database.models import User_setting, Parser_data
from app.database.session import get_db
from app.parser.parser_regulation import parsing_project, parsing
from app import get_bot

scheduler = None

async def send_new_npa():
    print('start sending')
    db = next(get_db())
    bot = get_bot()
    users = db.query(User_setting).filter_by(on_off=True).all()
    npas = db.query(Parser_data).filter_by(document_send=False).all()
    messege_text = 'Уведомление о начавшихся обсуждениях:'
    if npas is not None:
        for npa in npas:
            dict_data_npa = await parsing_project(npa.document_id)
            text = f'\n\nНаименование НПА: {dict_data_npa['title']}\nРазработчик: {dict_data_npa['department']}\nВид проекта: {dict_data_npa['kind']}\nНачало публичного обсуждения: {dict_data_npa['startDiscussion'][:10].replace('-', '.')} {dict_data_npa['startDiscussion'][11:19]}\nКонец публичного обсуждения: {dict_data_npa['endDiscussion'][:10].replace('-', '.')} {dict_data_npa['endDiscussion'][11:19]}\nСсылка на проект: {dict_data_npa['url']}'
            messege_text = messege_text + text
            npa.document_send = True
            db.commit()
        for u in users:
            await bot.send_message(text=messege_text[:4000], user_id=u.max_id)
        print('Рассылка завершена')
    else:
        print('Нет новых НПА')
            

async def start_scheduler():
    global scheduler
    scheduler = AsyncIOScheduler()
    
    scheduler.add_job(
        send_new_npa,
        trigger='cron',
        minute='5',
        id="send_new_npa"
    )

    scheduler.add_job(
        parsing,
        trigger='cron',
        minute='50',
        id="parsing"
    )
    
    scheduler.start()
    print("Scheduler started")