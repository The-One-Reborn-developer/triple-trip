import logging

from sqlalchemy import select

from app.database.models.users import User
from app.database.models.sync_session import sync_session


def get_user_admin(telegram_id: int) -> User:
    try:
        with sync_session() as session:
            with session.begin():
                user = session.scalar(select(User)
                                      .where(User.telegram_id == telegram_id and User.is_admin == True))

                if user:
                    logging.info(f'User {telegram_id} found in the database')
                    return user
                else:
                    logging.info(f'User {telegram_id} not found in the database')
                    return None
    except Exception as e:
        logging.error(f'Error in get_user getting user from database: {e}')
        return None