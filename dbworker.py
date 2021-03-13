import pymysql
from pymysql.cursors import DictCursor
from tgbot.database import connect


def open_close_connection(qsl_query_func):
    def open_close(**kwargs):
        connection = connect()
        cursor = connection.cursor()
        try:
            response = qsl_query_func(**kwargs, cursor=cursor)
        finally:
            pass
        connection.commit()
        connection.close()
        return response
    return open_close


@open_close_connection
def get_all_districts(cursor=None):
    cursor.execute('SELECT id, Name FROM district')
    return cursor.fetchall()


@open_close_connection
def get_all_disciplines(cursor=None):
    cursor.execute('SELECT id, Name FROM discipline')
    return cursor.fetchall()


@open_close_connection
def get_trainers(discipline=None, district=None, cursor=None):
    cursor.execute(
        '''
        SELECT user.fName, user.lName, trainer.id
        FROM user JOIN trainer 
        ON trainer.user_id = user.id
        WHERE trainer.discipline_id = %s
        ''', (discipline,))   
    trainers = cursor.fetchall()
    return trainers


# @open_close_connection
# def get_workouts(disipline=None, district=None, trainer=None, cursor=None):
#     print(disipline),
#     print(district),
#     print(trainer)
#     cursor.execute('SELECT id FROM discipline WHERE discipline.Name = %s', (disipline,))
#     disipline_id = cursor.fetchone()
#     print(disipline_id)
    
#     cursor.execute(
#         '''
#         SELECT 
#             workout.id,
#             workout_template.description, 
#             workout_template.trainer_id, 
#             workout_template.discipline_id, 
#             workout.time,
#             workout.date,
#             workout.members,
#             workout.max_capacity
#         FROM workout LEFT JOIN workout_template
#         ON workout_template.id = workout.template_id 
#         WHERE workout_template.trainer_id = %s AND workout_template.district_id = %s
#         ''', (trainer, district))
#     workouts = cursor.fetchall()
#     return workouts


@open_close_connection
def get_workouts(disipline=None, district=None, trainer=None, cursor=None):
    print(disipline),
    print(district),
    print(trainer)
    
    cursor.execute(
        '''
        SELECT district.Name
        FROM district
        WHERE district.id = %s
        ''', (district,)
    )
    district_name = cursor.fetchone()
    
    cursor.execute(
        '''
        SELECT user.fName, user.lName
        FROM trainer JOIN user
        ON trainer.user_id = user.id
        WHERE trainer.id = %s
        ''', (trainer,)
        )
    trainer_name = cursor.fetchall()
    
    cursor.execute(
        '''
        SELECT workout_template.description
        FROM workout_template
        WHERE workout_template.trainer_id = %s            
        ''', (trainer,)
    )
    workouts = cursor.fetchall()

    result = {
        'district': district_name,
        'trainer': trainer_name,
        'workout': workouts
    }
    return trainer_name, district_name, workouts