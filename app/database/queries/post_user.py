import logging
import os

from sqlalchemy import select

from app.database.models.users import User
from app.database.models.sync_session import sync_session


def post_user(telegram_id: int) -> bool:
    try:
        with sync_session() as session:
            with session.begin():
                user = session.scalar(select(User)
                                      .where(User.telegram_id == telegram_id))

                if not user:
                    admins_telegram_ids = os.getenv('ADMINS_TELEGRAM_IDS').split(',')
                    if str(telegram_id) in admins_telegram_ids:
                        user = User(telegram_id=telegram_id, is_admin=True)
                        session.add(user)

                        return True
                    else:
                        user = User(telegram_id=telegram_id)
                        session.add(user)

                        return True
                else:
                    logging.info(f'User {telegram_id} already exists in the database')
                    return False
    except Exception as e:
        logging.error(f'Error in post_user adding user to database: {e}')
        return False