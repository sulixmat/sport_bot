import os
print(__name__, os.getcwd())

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .dbworker import get_all_districts, get_all_disciplines, get_trainers, get_workouts

from aiogram.utils.callback_data import CallbackData


# levels = district, discipline, trainer
find_trainer_menu = CallbackData('find_trainer', 'level', 'district', 'discipline', 'trainer', 'workout')

def make_callback_data(level, district=0, discipline=0, trainer=0, workout=0):
    return find_trainer_menu.new(
        level=level,
        district=district,
        discipline=discipline,
        trainer=trainer,
        workout=workout
    )


async def district_keyboard() -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(row_width=1)
    
    districts = get_all_districts()
    
    for district in districts:
        button_text = district['Name']
        district_id = district['id']
        
        callback_data = make_callback_data(
            level=CURRENT_LEVEL+1,
            district=district_id
            )

        markup.insert(
            InlineKeyboardButton(
                text=button_text,
                callback_data=callback_data,
            )
        )
    
    
    markup.row(
        InlineKeyboardButton(
            text='Не имеет значения',
            callback_data=make_callback_data(
                level=CURRENT_LEVEL+1,
                district=0
                )
        )
    )
    return markup


async def discipline_keyboard(district) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=1)
    
    disciplines = get_all_disciplines()
    
    for discipline in disciplines:
        button_text = discipline['Name']
        discipline_id = discipline['id']
        
        callback_data = make_callback_data(
            level=CURRENT_LEVEL+1,
            discipline=discipline_id,
            district=district
            )

        markup.insert(
            InlineKeyboardButton(
                text=button_text,
                callback_data=callback_data,
            )
        )
    markup.row(
        InlineKeyboardButton(
            text='◀️ Назад', 
            callback_data=make_callback_data(level=CURRENT_LEVEL-1))
    )
    
    return markup


async def trainer_keyboard(district, discipline):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup(row_width=1)
    
    trainers = get_trainers(discipline=discipline, district=district)

    
    for trainer in trainers:
        trainer_f_name = trainer['fName']
        trainer_l_name = trainer['lName']
        trainer_id = trainer['id']
        
        button_text = f'{trainer_f_name} {trainer_l_name}'
        
        callback_data = make_callback_data(
            level=CURRENT_LEVEL+1,
            discipline=discipline,
            district=district,
            trainer=trainer_id
            )

        markup.insert(
            InlineKeyboardButton(
                text=button_text,
                callback_data=callback_data,
            )
        )
        
    markup.row(
        InlineKeyboardButton(
            text='◀️ Назад',
            callback_data=make_callback_data(
                level=CURRENT_LEVEL-1,
                district=district
            )
        )
    )
    return markup


async def workout_keyboard(district, discipline, trainer):
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup(row_width=1)
    trainer_name, district_name, workouts = get_workouts(disipline=discipline, district=district, trainer=trainer)
    print("START")
    print(district_name)
    print(trainer_name)
    print(workouts)
    print("END")
    trainer_f_name = trainer_name[0]['fName']
    trainer_l_name = trainer_name[0]['lName']
    try:
        district = district_name['Name']
    except:
        pass
    
    for workout in workouts:
        # workout_id          = workout['id']
        workout_description = workout['description']
        # workout_time        = workout['time']
        # workout_date        = workout['date']
        # workout_members     = ['members']
        # workout_capacity    = workout['capacity']
        
        button_text = 'Какая-то тренировка тренера'
        
        callback_data = make_callback_data(
            level=CURRENT_LEVEL+1,
            discipline=discipline,
            district=district,
            trainer=trainer,
            # workout=workout_id
        )
        
        markup.insert(
            InlineKeyboardButton(
                text=button_text,
                callback_data=callback_data,
            )
        )
        
    markup.row(
        InlineKeyboardButton(
            text='◀️ Назад',
            callback_data=make_callback_data(level=CURRENT_LEVEL-1, district=district, discipline=discipline)
        )
    )
    return markup

if __name__ == '__main__':
    pass
    
