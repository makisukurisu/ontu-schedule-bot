"""Contains some handy decorators for bot"""
from telegram import Update


def _print(exception: Exception):
    """Print exception for methods"""
    print(f"Виникла помилка:\n{exception.args}")


def reply_with_exception(func):
    """
    If while processing a call ValueError occurs - tries to reply with text to a message
    """
    async def inner(*args, **kwargs):
        try:
            value = await func(*args, **kwargs)
            return value
        except ValueError as exception:
            update = kwargs.pop("update", None)
            for arg in args:
                if isinstance(arg, Update):
                    update = arg

            if not update or not isinstance(update, Update):
                return _print(exception)

            query = update.callback_query
            message = None

            if update.message:
                message = update.message
            if query and query.message:
                message = query.message

            if not message:
                return _print(exception)
            await message.reply_text(
                f"Виникла помилка:\n{exception.args}"
            )
    return inner
