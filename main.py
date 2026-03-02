import asyncio
import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import bot, router
from services.reminder_service import reminders_worker


async def main():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    reminder_task = asyncio.create_task(reminders_worker(bot))
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        reminder_task.cancel()
        await asyncio.gather(reminder_task, return_exceptions=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

