from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from aiogram_dialog import DialogManager, StartMode, ShowMode

from misc.states import HomeDialogSG

home_router = Router()


@home_router.message(Command("start"))
async def start_command_handler(message: Message, dialog_manager: DialogManager):
    user_language_code: str = message.from_user.language_code
    await dialog_manager.start(HomeDialogSG.HOME, mode=StartMode.RESET_STACK,
                               show_mode=ShowMode.SEND)
    dialog_manager.dialog_data["user_language_code"] = user_language_code


@home_router.message(Command("help"))
async def help_command_handler(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(HomeDialogSG.HELP, mode=StartMode.RESET_STACK,
                               show_mode=ShowMode.SEND)


@home_router.message(Command("about"))
async def about_command_handler(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(HomeDialogSG.ABOUT, mode=StartMode.RESET_STACK,
                               show_mode=ShowMode.SEND)


@home_router.message(Command("settings"))
async def settings_command_handler(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(HomeDialogSG.SETTINGS, mode=StartMode.RESET_STACK,
                               show_mode=ShowMode.SEND)

