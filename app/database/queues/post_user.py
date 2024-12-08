import logging

from sqlalchemy import select

from app.database.models.users import User
from app.database.models.async_session import async_session


async def post_user(telegram_id: int) -> bool:
    with async_session() as session:
        try:
            user = session.scalar(select(User).where(User.telegram_id == telegram_id))

            if not user:
                user = User(telegram_id=telegram_id)
                session.add(user)

            return True
        except Exception as e:
            logging.error(f'Error creating user: {e}')
            return False