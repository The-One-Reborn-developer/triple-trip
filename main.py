import os
import logging
import asyncio
import time

from aiogram import Bot, Dispatcher

from dotenv import load_dotenv, find_dotenv

from app.routes.start import start_router
from app.routes.menu_ru import menu_router_ru
from app.routes.menu_en import menu_router_en
from app.routes.add_place_ru import add_place_ru_router
from app.routes.add_place_en import add_place_en_router
from app.routes.add_place_choose_country_ru import add_place_choose_country_ru_router
from app.routes.add_place_choose_country_en import add_place_choose_country_en_router
from app.routes.show_place_choose_country_ru import show_place_choose_country_ru_router
from app.routes.show_place_choose_country_en import show_place_choose_country_en_router
from app.routes.admin import admin_router
from app.routes.show_place_ru import show_place_ru_router
from app.routes.show_place_en import show_place_en_router

from app.tasks.create_tables_producer import create_tables_producer

load_dotenv(find_dotenv())


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    try:
        logging.info('Waiting for RabbitMQ to be ready')
        time.sleep(35)
        logging.info('Creating database tables')
        create_tables_producer()
    except Exception as e:
        logging.error(f'Error in main creating database tables: {e}')

    logging.info('Starting bot')
    bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
    dp = Dispatcher()
    dp.include_routers(
        start_router,
        menu_router_ru,
        menu_router_en,
        add_place_ru_router,
        add_place_en_router,
        add_place_choose_country_ru_router,
        add_place_choose_country_en_router,
        show_place_choose_country_ru_router,
        show_place_choose_country_en_router,
        admin_router,
        show_place_ru_router,
        show_place_en_router
    )

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info('Bot stopped')