import os
import logging
import asyncio

from aiogram import Bot, Dispatcher

from dotenv import load_dotenv, find_dotenv

from app.routes.start import start_router

from app.tasks.create_tables_producer import create_tables_producer

load_dotenv(find_dotenv())


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    try:
        logging.info('Creating database tables')
        create_tables_producer()
    except Exception as e:
        logging.error(f'Error in main creating database tables: {e}')

    logging.info('Starting bot')
    bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
    dp = Dispatcher()
    dp.include_routers(
        start_router
    )

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info('Bot stopped')