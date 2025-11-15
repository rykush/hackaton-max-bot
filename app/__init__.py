import aiomax
import asyncio
from config import Config

bot = aiomax.Bot(Config.TOKEN, default_format="markdown")

def get_bot():
    return bot

async def create_app():
    from app.routes import router as main_router
    bot.add_router(main_router)
    
    from app.platforms import pl_router
    bot.add_router(pl_router)
    
    from app.ping import op_router
    bot.add_router(op_router)
    
    from app.handbook import sp_router
    bot.add_router(sp_router)
    
    from app.ping.scheduler import start_scheduler
    await start_scheduler()
    
    # Запуск бота
    await bot.start_polling()

    
