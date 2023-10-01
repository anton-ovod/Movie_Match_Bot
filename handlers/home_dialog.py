import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from aiogram_dialog import DialogManager, StartMode, ShowMode

from dialogs.home_dialog import HomeDialogSG, main_dialog

home_router = Router()
home_router.include_router(main_dialog)


@home_router.message(Command("start"))
async def start_command_handler(message: Message, dialog_manager: DialogManager):
    logging.info("Start command received")
    await dialog_manager.start(HomeDialogSG.home, mode=StartMode.RESET_STACK,
                               show_mode=ShowMode.SEND)


@home_router.message(Command("help"))
async def help_command_handler(message: Message, dialog_manager: DialogManager):
    logging.info("Help command received")
    await dialog_manager.start(HomeDialogSG.help, mode=StartMode.RESET_STACK,
                               show_mode=ShowMode.SEND)


@home_router.message(Command("about"))
async def about_command_handler(message: Message, dialog_manager: DialogManager):
    logging.info("About command received")
    await dialog_manager.start(HomeDialogSG.about, mode=StartMode.RESET_STACK,
                               show_mode=ShowMode.SEND)


@home_router.message(Command("settings"))
async def settings_command_handler(message: Message, dialog_manager: DialogManager):
    logging.info("Settings command received")
    await dialog_manager.start(HomeDialogSG.settings, mode=StartMode.RESET_STACK,
                               show_mode=ShowMode.SEND)



