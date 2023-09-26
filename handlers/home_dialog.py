import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from aiogram_dialog import DialogManager, StartMode

from dialogs.main_dialog import MainDialogSG, main_dialog

home_router = Router()
home_router.include_router(main_dialog)


@home_router.message(Command("start"))
async def start_command_handler(message: Message, dialog_manager: DialogManager):
    logging.info("Start command received")
    await dialog_manager.start(MainDialogSG.home, mode=StartMode.RESET_STACK)
