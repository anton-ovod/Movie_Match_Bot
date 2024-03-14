from aiogram.types import Message
from aiogram_dialog import ShowMode, DialogManager

from dialogs.searching import env

unknown_type_message = env.get_template("common/unknown_type_message.jinja2").render()


async def message_handler(message: Message, _, dialog_manager: DialogManager):
    dialog_manager.show_mode = ShowMode.EDIT
    await message.delete()


async def unknown_message_handler(message: Message, *args):
    await message.answer(text=unknown_type_message, parse_mode="HTML")
