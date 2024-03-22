from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Group, Select, Keyboard
from aiogram_dialog.widgets.text import Format

from misc.enums import HomeDialogOptions, SearchDialogOptions


async def home_menu_button_on_click(callback: CallbackQuery,
                                    _,
                                    manager: DialogManager,
                                    button_id: str):
    enum_object = getattr(HomeDialogOptions, button_id)
    await manager.switch_to(enum_object.state, show_mode=ShowMode.EDIT)
    await callback.answer(f"{enum_object.emoji} {enum_object.title}")


def get_home_dialog_keyboard() -> Keyboard:
    current_home_enums = list(HomeDialogOptions)

    home_dialog_keyboard = Group(
        Select(
            Format("{item.emoji}  {item.title}"),
            id="home_menu_buttons",
            item_id_getter=lambda item: item.name,
            items=current_home_enums,
            on_click=home_menu_button_on_click
        ),
        width=2
    )

    return home_dialog_keyboard


async def searching_options_button_on_click(callback: CallbackQuery,
                                            _,
                                            manager: DialogManager,
                                            button_id: str):
    enum_object = getattr(SearchDialogOptions, button_id)
    await manager.start(enum_object.state, show_mode=ShowMode.EDIT)
    manager.dialog_data["subject_type"] = enum_object.name
    await callback.answer(f"🤖 I'm ready to search for {enum_object.emoji} {enum_object.name.lower().capitalize()}s!")


def get_searching_options_keyboard() -> Keyboard:
    current_searching_enums = list(SearchDialogOptions)

    searching_options_keyboard = Group(
        Select(
            Format("{item.emoji} {item.title}"),
            id="searching_options_buttons",
            item_id_getter=lambda item: item.name,
            items=current_searching_enums,
            on_click=searching_options_button_on_click
        ),
        width=3
    )

    return searching_options_keyboard
