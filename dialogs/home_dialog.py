import logging

from aiogram.filters.state import State, StatesGroup
from aiogram.types import Message

from aiogram_dialog import Window, Dialog, DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Group, SwitchTo, Row
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const

from dialogs import env

from .searching.movie_dialog import MovieDialogSG
from .searching.tvshow_dialog import ShowDialogSG
from .searching.person_dialog import PersonDialogSG

from handlers.searching.movie_dialog import init_movie_search_dialog

home_message = env.get_template("home_message.jinja2").render()
about_message = env.get_template("about_message.jinja2").render()
help_message = env.get_template("help_message.jinja2").render()
settings_message = env.get_template("settings_message.jinja2").render()
search_message = env.get_template("options_message.jinja2").render()


class HomeDialogSG(StatesGroup):
    home = State()
    about = State()
    help = State()
    settings = State()
    search = State()
    cinema = State()
    discover = State()


home_buttons_group = Group(
    SwitchTo(Const("❓  Help"), id="help", state=HomeDialogSG.help,
             on_click=lambda callback, self, manager: callback.answer("❓ Help")),
    SwitchTo(Const("📚  About"), id="about", state=HomeDialogSG.about,
             on_click=lambda callback, self, manager: callback.answer("📚 About")),
    SwitchTo(Const("🔍  Search"), id="search", state=HomeDialogSG.search,
             on_click=lambda callback, self, manager: callback.answer("🔍 Search")),
    SwitchTo(Const("🍿  Cinema"), id="cinema", state=HomeDialogSG.cinema,
             on_click=lambda callback, self, manager: callback.answer("🍿 Cinema")),
    SwitchTo(Const("🌟  Discover"), id="discover", state=HomeDialogSG.discover,
             on_click=lambda callback, self, manager: callback.answer("🌟 Discover")),
    SwitchTo(Const("⚙️  Settings"), id="settings", state=HomeDialogSG.settings,
             on_click=lambda callback, self, manager: callback.answer("⚙️ Settings")),
    width=2
)
search_options_group = Group(
    Row(
        SwitchTo(Const("🎬  Movie"), id="movie", state=MovieDialogSG.title_request,
                 on_click=init_movie_search_dialog),
        SwitchTo(Const("📺  Show"), id="show", state=ShowDialogSG.title_request,
                 on_click=lambda callback, self, manager: callback.answer("📺 Show")),
        SwitchTo(Const("👤  Person"), id="person", state=PersonDialogSG.name_request,
                 on_click=lambda callback, self, manager: callback.answer("👤 Person"))
    ),
    SwitchTo(Const("⬅️  Back"), id="home", state=HomeDialogSG.home,
             on_click=lambda callback, self, manager: callback.answer("🏠 Home")),

)


async def message_handler(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
    logging.info(f"Message from '{message.from_user.username}' received: '{message.text}'")
    dialog_manager.show_mode = ShowMode.EDIT
    await message.delete()


main_dialog = Dialog(
    Window(
        home_message,
        home_buttons_group,
        MessageInput(message_handler),
        parse_mode="HTML",
        state=HomeDialogSG.home,
        disable_web_page_preview=True
    ),
    Window(
        about_message,
        SwitchTo(Const("🏠 Home"), id="home", state=HomeDialogSG.home,
                 on_click=lambda callback, self, manager: callback.answer("🏠 Home")),
        MessageInput(message_handler),
        parse_mode="HTML",
        state=HomeDialogSG.about,
        disable_web_page_preview=True
    ),
    Window(
        help_message,
        SwitchTo(Const("🏠 Home"), id="home", state=HomeDialogSG.home,
                 on_click=lambda callback, self, manager: callback.answer("🏠 Home")),
        MessageInput(message_handler),
        parse_mode="HTML",
        state=HomeDialogSG.help,
        disable_web_page_preview=True
    ),
    Window(
        settings_message,
        SwitchTo(Const("🏠 Home"), id="home", state=HomeDialogSG.home,
                 on_click=lambda callback, self, manager: callback.answer("🏠 Home")),
        MessageInput(message_handler),
        parse_mode="HTML",
        state=HomeDialogSG.settings,
        disable_web_page_preview=True
    ),
    Window(
        search_message,
        search_options_group,
        MessageInput(message_handler),
        parse_mode="HTML",
        state=HomeDialogSG.search,
        disable_web_page_preview=True
    )
)
