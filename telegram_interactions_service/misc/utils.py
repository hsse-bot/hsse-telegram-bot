from .dataclasses import User


def generate_user_profile_text(user: User) -> str:
    if user.student_info is not None:
        sex = 'мужской' if user.student_info.isMale else 'женский'
    else:
        sex = "-"
    return f'''
        Фамилия: {user.surname}
        Имя: {user.name}
        Почта: {user.email}
        Телеграм id: {user.tg_id}
        Очки активизма: {user.score}
        Пол: {sex}
        Группа: {user.student_info.groupNumber if user.student_info is not None else "-"}
        Номер комнаты: {user.student_info.roomNumber if user.student_info is not None else "-"}
    '''
