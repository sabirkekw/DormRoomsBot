import logging
from typing import Any, Callable, Dict, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

def init_logger():
    py_logger = logging.getLogger("log")
    py_logger.setLevel(logging.INFO)
    py_handler = logging.FileHandler("app/logs/log.log", mode='w')
    py_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
    py_handler.setFormatter(py_formatter)
    py_logger.addHandler(py_handler)

# inner middleware for logging messages
class LogMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        py_logger = logging.getLogger("log")
        try:
            result = await handler(event, data)
            py_logger.info(f"{event.from_user.first_name} @{event.from_user.username} {event.text}")
            return result
        except Exception as e:
            py_logger.critical(f"{event.from_user.first_name} @{event.from_user.username} {event.text}", exc_info=True)
        return 