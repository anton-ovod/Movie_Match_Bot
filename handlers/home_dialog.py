import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.input import MessageInput

from misc.states import HomeDialogSG

home_router = Router()


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


async def message_handler(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
    logging.info(f"Message from '{message.from_user.username}' received: '{message.text}'")
    dialog_manager.show_mode = ShowMode.EDIT
    await message.delete()
