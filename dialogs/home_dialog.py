from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import SwitchTo
from aiogram_dialog.widgets.text import Const

from dialogs import env
from handlers.messages_handlers import message_handler
from keyboards.home_keyboards import (get_home_dialog_keyboard,
                                      get_searching_options_keyboard)

from misc.states import HomeDialogSG

home_message = env.get_template("home_message.jinja2").render()
about_message = env.get_template("about_message.jinja2").render()
help_message = env.get_template("help_message.jinja2").render()
settings_message = env.get_template("settings_message.jinja2").render()
search_message = env.get_template("options_message.jinja2").render()

home_dialog = Dialog(
    Window(
        home_message,
        get_home_dialog_keyboard(),
        MessageInput(message_handler),
        parse_mode="HTML",
        state=HomeDialogSG.HOME,
        disable_web_page_preview=True
    ),
    Window(
        about_message,
        SwitchTo(
            Const("🏠 Home"),
            id="home",
            state=HomeDialogSG.HOME),
        MessageInput(message_handler),
        parse_mode="HTML",
        state=HomeDialogSG.ABOUT,
        disable_web_page_preview=True
    ),
    Window(
        help_message,
        SwitchTo(
            Const("🏠 Home"),
            id="home",
            state=HomeDialogSG.HOME
        ),
        MessageInput(message_handler),
        parse_mode="HTML",
        state=HomeDialogSG.HELP,
        disable_web_page_preview=True
    ),
    Window(
        settings_message,
        SwitchTo(
            Const("🏠 Home"),
            id="home",
            state=HomeDialogSG.HOME),
        MessageInput(message_handler),
        parse_mode="HTML",
        state=HomeDialogSG.SETTINGS,
        disable_web_page_preview=True
    ),
    Window(
        search_message,
        get_searching_options_keyboard(),
        SwitchTo(
            Const("⬅️  Back"),
            id="home",
            state=HomeDialogSG.HOME
        ),
        MessageInput(message_handler),
        parse_mode="HTML",
        state=HomeDialogSG.SEARCH,
        disable_web_page_preview=True
    )
)
