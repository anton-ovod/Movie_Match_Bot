from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Group, SwitchTo, Row
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const

from dialogs import env

from misc.states import HomeDialogSG, MovieDialogSG, ShowDialogSG, PersonDialogSG

from handlers.searching.movie_dialog import init_movie_search_dialog
from handlers.searching.tvshow_dialog import init_tvshow_search_dialog
from handlers.home_dialog import message_handler

home_message = env.get_template("home_message.jinja2").render()
about_message = env.get_template("about_message.jinja2").render()
help_message = env.get_template("help_message.jinja2").render()
settings_message = env.get_template("settings_message.jinja2").render()
search_message = env.get_template("options_message.jinja2").render()

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
                 on_click=init_tvshow_search_dialog),
        SwitchTo(Const("👤  Person"), id="person", state=PersonDialogSG.name_request,
                 on_click=lambda callback, self, manager: callback.answer("👤 Person"))
    ),
    SwitchTo(Const("⬅️  Back"), id="home", state=HomeDialogSG.home,
             on_click=lambda callback, self, manager: callback.answer("🏠 Home")),

)

home_dialog = Dialog(
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
