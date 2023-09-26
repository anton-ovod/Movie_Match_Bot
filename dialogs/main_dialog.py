from aiogram.filters.state import State, StatesGroup

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Group, SwitchTo
from aiogram_dialog.widgets.text import Const

from aiogram_dialog import Dialog

from dialogs import env

home_message = env.get_template("home_message.jinja2").render()
about_message = env.get_template("about_message.jinja2").render()
help_message = env.get_template("help_message.jinja2").render()
settings_message = env.get_template("settings_message.jinja2").render()


class MainDialogSG(StatesGroup):
    home = State()
    about = State()
    help = State()
    settings = State()


home_buttons_group = Group(
    SwitchTo(Const("❓  Help"), id="help", state=MainDialogSG.help),
    SwitchTo(Const("📚  About"), id="about", state=MainDialogSG.about),
    SwitchTo(Const("🔍  Search"), id="search", state=MainDialogSG.home),
    SwitchTo(Const("🍿  Cinema"), id="cinema", state=MainDialogSG.home),
    SwitchTo(Const("🌟  Discover"), id="discover", state=MainDialogSG.home),
    SwitchTo(Const("⚙️  Settings"), id="settings", state=MainDialogSG.settings),
    width=2
)

main_dialog = Dialog(
    Window(
        home_message,
        home_buttons_group,
        parse_mode="HTML",
        state=MainDialogSG.home,
        disable_web_page_preview=True
    ),
    Window(
        about_message,
        SwitchTo(Const("🏠 Home"), id="home", state=MainDialogSG.home),
        parse_mode="HTML",
        state=MainDialogSG.about,
        disable_web_page_preview=True
    ),
    Window(
        help_message,
        SwitchTo(Const("🏠 Home"), id="home", state=MainDialogSG.home),
        parse_mode="HTML",
        state=MainDialogSG.help,
        disable_web_page_preview=True
    ),
    Window(
        settings_message,
        SwitchTo(Const("🏠 Home"), id="home", state=MainDialogSG.home),
        parse_mode="HTML",
        state=MainDialogSG.settings,
        disable_web_page_preview=True
    )
)
