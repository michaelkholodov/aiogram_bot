from datetime import datetime
from typing import Callable, Dict, Any, Awaitable
from dateutil.parser import parse
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery


class TimeRestrictionMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        current_time = datetime.now()
        allowed_start_time = parse('10:00')
        allowed_end_time = parse('23:59')

        if not allowed_start_time <= current_time <= allowed_end_time:
            await event.answer("Sorry, the bot is only available between 10 AM and 10 PM.")
            return
        return await handler(event, data)
