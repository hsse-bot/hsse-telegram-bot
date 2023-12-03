from typing import NoReturn, List

import aiohttp

from ..config import DEBUG_MODE
from telegram_interactions_service.services_interactions import interactions_interfaces
from ..misc.dataclasses import User, Form, Role, StudentInfo, UserDelta, FormTicket, RegistrationUserData
from .paths import user_service_api_url
from ..exceptions import UserManagingServiceError


class UserManagingServiceInteraction(interactions_interfaces.UserManagingServiceInteractionInterface):
    async def get_role_id(self, role_name: str) -> int:
        #TODO
        raise Exception('this method is not finished')

    async def add_user_to_database(self, user: RegistrationUserData) -> NoReturn:
        if DEBUG_MODE:
            return
        #TODO
        user_role_id = self.get_role_id(role_name='user')
        async with aiohttp.ClientSession() as session:
            async with session.post(user_service_api_url + 'create-user',
                                    json={"tgId": user.tg_id, "name": user.name, "surname": user.surname,
                                          "roleId": user_role_id}) as response:
                if response.status != 200:
                    raise UserManagingServiceError(f'response status is {response.status} (not 200)')

    async def set_user_role(self, user: User, new_role: Role) -> NoReturn:
        pass

    async def add_admin(self, user: User) -> NoReturn:
        pass

    async def get_score(self, user: User) -> int | None:
        pass

    async def update_user(self, user: User, new_user_data: UserDelta) -> NoReturn:
        if DEBUG_MODE:
            return
        async with aiohttp.ClientSession() as session:
            async with session.put(user_service_api_url + 'update-user', params={'tgId': user.tg_id},
                                   json={'newName': new_user_data.new_name, 'newSurname': new_user_data.new_surname,
                                         'newRoleId': new_user_data.new_role_id,
                                         'studentInfoDelta': {
                                           'newRoomNumber': new_user_data.student_info_delta.room_number,
                                           'newIsMale': new_user_data.student_info_delta.is_male},
                                         'newScore': new_user_data.new_score}) as response:
                if response.status == 400:
                    return
                if response.status != 200:
                    raise UserManagingServiceError(f'response status is {response.status} (not 200)')

    async def get_top_scores(self) -> List[User] | None:
        pass

    async def get_user_role(self, user: User) -> Role | None:
        pass

    async def get_user(self, tg_id: int) -> User | None:
        if DEBUG_MODE:
            role = Role(id=1, name='test')
            student_info = StudentInfo(room_number=411,
                                       is_male=True)
            return User(name='Тестировщик', surname='Тестов', tg_id=12345678, role=role,
                        score='100', student_info=student_info)
        async with aiohttp.ClientSession() as session:
            async with session.get(user_service_api_url + 'get-user', params={'tgId': tg_id}) as response:
                if response.status == 400:
                    return
                if response.status != 200:
                    raise UserManagingServiceError(f'response status is {response.status} (not 200)')
                data = await response.json()
                try:
                    role = Role(id=data['role']['id'], name=data['role']['name'])
                    student_info = StudentInfo(room_number=data['studentInfo']['roomNumber'],
                                               is_male=data['studentInfo']['isMale'])
                    return User(name=data['name'], surname=data['surname'], tg_id=data['tgId'], role=role,
                                score=data['score'], student_info=student_info)
                except KeyError:
                    raise UserManagingServiceError(f'bad data: {data}')

    async def is_admin(self, tg_id: int) -> bool:
        if DEBUG_MODE:
            return True
        #TODO
        raise Exception('this method is not finished')
