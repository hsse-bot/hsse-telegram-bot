from typing import NoReturn, List

import aiohttp

from ..config import DEBUG_MODE
from telegram_interactions_service.services_interactions import interactions_interfaces
from ..misc.dataclasses import User, Form, Role, StudentInfo, generate_student_info, UserDelta, \
    StudentInfoDelta, generate_delta_student_info, FormTicket, RegistrationUserData, Admin
from ..misc import constants
from .paths import user_service_api_url
from ..exceptions import UserManagingServiceError, EmailAlreadyUsed


class UserManagingServiceInteraction(interactions_interfaces.UserManagingServiceInteractionInterface):
    async def get_role_id(self, role_name: str) -> int:
        async with aiohttp.ClientSession() as session:
            async with session.get(user_service_api_url + 'get-role-by-name', params={'name': role_name}) as response:
                if response.status == 200:
                    try:

                        data = await response.json()
                    except Exception as error:
                        raise UserManagingServiceError(f'Response with status {response.status} has no json.\n Error:"{error}"')
                    return data['id']
                raise UserManagingServiceError(f'response status is {response.status} (not 200)')

    async def get_user(self, tg_id: int) -> User | None:
        if DEBUG_MODE:
            return
            role = Role(id=1, name=constants.USER_ROLE_NAME)
            student_info = generate_student_info({"roomNumber": 411, "isMale": True, "groupNumber": "Б13-303"})
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
                    student_info = generate_student_info(data['studentInfo'])
                    return User(name=data['name'], surname=data['surname'], tg_id=data['tgId'], role=role,
                                score=data['score'], student_info=student_info)
                except KeyError:
                    raise UserManagingServiceError(f'bad data: {data}')

    async def get_all_users(self) -> List[User]:
        if DEBUG_MODE:
            user_role = Role(id=1, name=constants.USER_ROLE_NAME)
            student_info1 = generate_student_info({"roomNumber": 411, "isMale": True, "groupNumber": "Б13-303"})
            student_info2 = generate_student_info({"roomNumber": 110, "isMale": True, "groupNumber": "Б13-303"})
            return [
                User(name='Тестировщик', surname='Тестов', tg_id=12345678, role=user_role,
                     score='100', student_info=student_info1),

                User(name='Друг', surname='Тестировщика', tg_id=99999999, role=user_role,
                     score='50', student_info=student_info2),

                User(name='Друг', surname='Тестировщика', tg_id=99999999, role=user_role,
                     score='0', student_info=student_info2),

                User(name='Друг', surname='Тестировщика', tg_id=99999999, role=user_role,
                     score='120', student_info=student_info2),

                User(name='Друг', surname='Тестировщика', tg_id=99999999, role=user_role,
                     score='10', student_info=student_info2),

                User(name='Друг', surname='Тестировщика', tg_id=99999999, role=user_role,
                     score='-10', student_info=student_info2),

                User(name='Александр', surname='Тюленев', tg_id=66666666, role=user_role,
                     score='2000', student_info=student_info2),
            ]
        async with aiohttp.ClientSession() as session:
            async with session.get(user_service_api_url + 'get-all-users') as response:
                if response.status != 200:
                    raise UserManagingServiceError(f'response status is {response.status} (not 200)')
                data = await response.json()
                list_of_users = []
                try:
                    for user_data in data:
                        role = Role(id=user_data['role']['id'], name=user_data['role']['name'])
                        student_info = generate_student_info(user_data['studentInfo'])
                        list_of_users.append(
                            User(name=user_data['name'], surname=user_data['surname'],
                                 tg_id=user_data['tgId'], role=role,
                                 score=user_data['score'], student_info=student_info)
                        )
                    return list_of_users
                except KeyError:
                    raise UserManagingServiceError(f'bad data: {data}')

    async def add_user_to_database(self, user: RegistrationUserData) -> NoReturn:
        if DEBUG_MODE:
            return
        user_role_id = self.get_role_id(role_name=constants.USER_ROLE_NAME)
        async with aiohttp.ClientSession() as session:
            async with session.post(user_service_api_url + 'create-user',
                                    json={'tgId': user.tg_id, 'name': user.name, 'surname': user.surname,
                                          'roleId': user_role_id}) as response:
                if response.status == 400:
                    try:
                        data = await response.json()
                    except Exception as error:
                        raise UserManagingServiceError(f'Response with status {response.status} has no json.\n Error:"{error}"')
                    if data['msg'] == constants.USER_SERVICE_400_STATUS_MSG_EXISTING_TG_ID_OR_EMAIL:
                        if self.get_user(tg_id=user.tg_id) is not None:
                            raise EmailAlreadyUsed()
                        raise UserManagingServiceError(f'Already exists user with tg_id:{user.tg_id}')
                    if data['msg'] == constants.USER_SERVICE_400_STATUS_MSG_ADDING_BANNED_USER:
                        raise UserManagingServiceError(f'User with tg_id:{user.tg_id} is banned')
                    raise UserManagingServiceError(f'Unknown error with code 400. Returned json: "{data}"')
                if response.status != 200:
                    raise UserManagingServiceError(f'response status is {response.status} (not 200)')

    async def update_user(self, tg_id: int, new_user_data: UserDelta) -> NoReturn:
        if DEBUG_MODE:
            return
        async with aiohttp.ClientSession() as session:
            async with session.put(user_service_api_url + 'update-user', params={'tgId': tg_id},
                                   json=new_user_data.model_dump_json()
                                   # json={'newName': new_user_data.new_name, 'newSurname': new_user_data.new_surname,
                                   #       'newRoleId': new_user_data.new_role_id,
                                   #       'studentInfoDelta': {
                                   #         'newRoomNumber': new_user_data.student_info_delta.room_number,
                                   #         'newIsMale': new_user_data.student_info_delta.is_male},
                                   #       'newScore': new_user_data.new_score
                                   #       }
                                   ) as response:
                if response.status == 400:
                    return
                if response.status != 200:
                    raise UserManagingServiceError(f'response status is {response.status} (not 200)')

    async def delete_user(self, tg_id: int) -> NoReturn:
        if DEBUG_MODE:
            return
        async with aiohttp.ClientSession() as session:
            async with session.delete(user_service_api_url + 'delete-user', params={'tgId': tg_id}) as response:
                if response.status != 200:
                    raise UserManagingServiceError(f'response status is {response.status} (not 200)')

    async def set_role(self, tg_id: int, new_role_id: int) -> NoReturn:
        await self.update_user(tg_id=tg_id, new_user_data=UserDelta(newRoleId=new_role_id))

    async def set_user_user_role(self, tg_id: int) -> NoReturn:
        user_role_id = await self.get_role_id(constants.USER_ROLE_NAME)
        await self.set_role(tg_id=tg_id, new_role_id=user_role_id)

    async def set_user_admin_role(self, tg_id: int) -> NoReturn:
        admin_role_id = await self.get_role_id(constants.ADMIN_ROLE_NAME)
        await self.set_role(tg_id=tg_id, new_role_id=admin_role_id)

    async def is_admin(self, tg_id: int) -> bool:  # role is admin, not role is super_admin
        if DEBUG_MODE:
            return True
        user = await self.get_user(tg_id)
        if user is None:
            return False
        return user.role.name == constants.ADMIN_ROLE_NAME

    async def get_admins(self) -> List[Admin]:
        if DEBUG_MODE:
            admins = [Admin(tg_id=595905860, note='Тестовый')]
            return admins
        all_users = await self.get_all_users()
        return list(filter(lambda user: user.role.name == constants.ADMIN_ROLE_NAME, all_users))

    async def get_top_scores(self) -> List[User] | None:
        all_users = await self.get_all_users()
        all_users.sort(key=lambda user: user.score, reverse=True)
        return all_users[:constants.SIZE_OF_USERS_TOP]

    async def add_activity_points(self, tg_id: int, points: int) -> NoReturn:
        await self.update_user(tg_id=tg_id, new_user_data=UserDelta(deltaScore=points))

    async def ban_user(self, tg_id: int) -> NoReturn:
        if DEBUG_MODE:
            return
        async with aiohttp.ClientSession() as session:
            async with session.post(user_service_api_url + 'ban-user', params={'tgId': tg_id}) as response:
                if response.status != 200:
                    raise UserManagingServiceError(f'response status is {response.status} (not 200)')

    async def is_banned(self, tg_id: int) -> bool:
        if DEBUG_MODE:
            return False
        async with aiohttp.ClientSession() as session:
            async with session.get(user_service_api_url + 'is-user-banned', params={'tgId': tg_id}) as response:
                if response.status != 200:
                    raise UserManagingServiceError(f'response status is {response.status} (not 200)')
                try:
                    data = await response.json()
                except Exception as error:
                    raise UserManagingServiceError(
                        f'Response with status {response.status} has no json.\n Error:"{error}"')
                return data['is banned']

    async def unban_user(self, tg_id: int) -> NoReturn:
        if DEBUG_MODE:
            return
        async with aiohttp.ClientSession() as session:
            async with session.delete(user_service_api_url + 'unban-user', params={'tgId': tg_id}) as response:
                if response.status != 200:
                    raise UserManagingServiceError(f'response status is {response.status} (not 200)')
