import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.main_keyboard import get_main_keyboard
from keyboards.search_keyboards import get_type_keyboard

from filters.callback_factories import BackCallbackFactory

router = Router()


@router.callback_query(BackCallbackFactory.filter())
async def callbacks_back(query: CallbackQuery, callback_data: BackCallbackFactory):
    logging.info(f"Callback query: {query.data}")
    if callback_data.to == "home":
        await query.message.edit_text("<b>Welcome to MovieMatcherBot!</b> 🎬🤖\n\n"
                                      "I'm here to help you find your perfect movie match.\n"
                                      "Whether you're in the mood for action-packed adventures or heartwarming "
                                      "romances, I've got you covered."
                                      "Just let me know your preferences, and I'll suggest the best movies for you.\n\n",
                                      reply_markup=get_main_keyboard())
    elif callback_data.to == "search":
        await query.message.edit_text(" 🔍  Search\n\n"
                                      "Choose what you want to search for:\n",
                                      reply_markup=get_type_keyboard())
    elif callback_data.to == "cinema":
        pass

    await query.answer("Ok, let's go back! 🤖")
