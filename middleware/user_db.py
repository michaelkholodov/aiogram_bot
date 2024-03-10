from datetime import datetime
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from orm.orm import SimpleORM
import logging

class UserDBMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:

        orm = SimpleORM('database2.db')
        orm.create_table('users', ['id INTEGER PRIMARY KEY', 'user_id INTEGER', 'user_name TEXT'])
        try:
            # Проверяем, есть ли пользователь уже в базе данных
            existing_user = orm.select('users', filters={'user_id': event.from_user.id})

            # Если пользователя нет, добавляем его в базу данных
            if not existing_user:
                new_user = orm.insert('users', {'user_id': event.from_user.id, 'user_name': event.from_user.first_name})
                logging.info(new_user)
        finally:
            orm.close()

