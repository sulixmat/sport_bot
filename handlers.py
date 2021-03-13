import logging
from typing import Union

from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ParseMode
from aiogram.utils import executor
import aiogram.utils.markdown as fmt
from aiogram import Bot, types
from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text

from tgbot.database import is_user_exist
from tgbot.config import FIND_WORKOUT_BUTTON
from .keyboards import district_keyboard, discipline_keyboard,trainer_keyboard, find_trainer_menu, workout_keyboard

logger = logging.getLogger(__name__)


async def list_districts(message: Union[types.Message, types.CallbackQuery], **kwargs):
    markup = await district_keyboard()
    
    if isinstance(message, types.Message):
        await message.reply(
            text='В каком районе города ищем тренировку?', 
            reply_markup=markup,
            reply=False,
            parse_mode=ParseMode.MARKDOWN
            )
    elif isinstance(message, types.CallbackQuery):
        call = message
        await call.message.edit_reply_markup(markup)


async def list_disciplines(call: types.CallbackQuery, district, **kwargs):
    markup = await discipline_keyboard(district)
    await call.message.edit_text(
        text='Каким видом спорта хотите заняться?',
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=markup
    )
    
    
async def list_trainers(call: types.CallbackQuery, district, discipline, **kwargs):
    markup = await trainer_keyboard(district=district, discipline=discipline)
    await call.message.edit_text(
        text='Выберите тренера!',
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=markup
    )
    
    
async def list_workouts(call: types.CallbackQuery, district, discipline, trainer, **kwargs):
    markup = await workout_keyboard(district=district, discipline=discipline, trainer=trainer)
    await call.message.edit_text(
        text='Тренировки выбранного тренера',
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=markup
    )
    

async def navigate(call: types.CallbackQuery, callback_data: dict):
    current_level   = callback_data.get('level')
    district        = callback_data.get('district')
    discipline      = callback_data.get('discipline')
    trainer         = callback_data.get('trainer')
    workout         = callback_data.get('workout')

    levels = {
        '0': list_districts,
        '1': list_disciplines,
        '2': list_trainers,
        '3': list_workouts
    }
    
    current_level_function = levels[current_level]
    
    await current_level_function(
        call, 
        district=district, 
        discipline=discipline, 
        trainer=trainer,
        workout=workout
        )

def find_workout(dp: Dispatcher):
    dp.register_message_handler(list_districts, Text(equals=FIND_WORKOUT_BUTTON))
    
    dp.register_callback_query_handler(navigate, find_trainer_menu.filter())