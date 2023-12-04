from typing import NoReturn, List

import aiohttp

from telegram_interactions_service.services_interactions.interactions_interfaces import \
    TelegramNotifierServiceInteractionInterface
from ..misc.dataclasses import User, NotifyCategory
from .paths import notify_service_api_url
from ..exceptions import TelegramNotifierServiceError
from ..config import DEBUG_MODE


class TelegramNotifierServiceInteraction(TelegramNotifierServiceInteractionInterface):

    async def notify(self, category: NotifyCategory, text: str) -> NoReturn:
        if DEBUG_MODE:
            return
        async with aiohttp.ClientSession() as session:
            async with session.post(notify_service_api_url + 'messaging/send',
                                    json={'text': text, 'categoryId': category.id}) as response:
                if response.status != 200:
                    raise TelegramNotifierServiceError(f'response status is {response.status} (not 200)')

    async def create_category(self, category: NotifyCategory) -> NoReturn:
        if DEBUG_MODE:
            return
        async with aiohttp.ClientSession() as session:
            async with session.post(notify_service_api_url + 'categories', json={'name': category.name}) as response:
                if response.status != 200:
                    raise TelegramNotifierServiceError(f'response status is {response.status} (not 200)')

    async def delete_category(self, category: NotifyCategory) -> NoReturn:
        if DEBUG_MODE:
            return
        async with aiohttp.ClientSession() as session:
            async with session.delete(notify_service_api_url + f'categories/{category.id}') as response:
                if response.status != 200:
                    raise TelegramNotifierServiceError(f'response status is {response.status} (not 200)')

    async def get_category(self, category_id: int) -> NotifyCategory:
        if DEBUG_MODE:
            return NotifyCategory(id=category_id, name=f'test category')
        async with aiohttp.ClientSession() as session:
            async with session.get(notify_service_api_url + f'categories/{category_id}') as response:
                if response.status != 200:
                    raise TelegramNotifierServiceError(f'response status is {response.status} (not 200)')
                response_json = await response.json()
                try:
                    return NotifyCategory(id=response_json['id'], name=response_json['name'])
                except KeyError as error:
                    raise TelegramNotifierServiceError(f'bad response data: "{response_json}"\n No key named {str(error)}')

    async def get_all_categories(self) -> List[NotifyCategory]:
        if DEBUG_MODE:
            return [NotifyCategory(id=i, name=f'category number {i}') for i in range(12)]
        async with aiohttp.ClientSession() as session:
            async with session.get(notify_service_api_url + 'categories') as response:
                if response.status != 200:
                    raise TelegramNotifierServiceError(f'response status is {response.status} (not 200)')
                response_json = await response.json()
                answer = []
                if isinstance(response_json, list):
                    for category_data in response_json:
                        answer.append(NotifyCategory(id=category_data['id'], name=category_data['name']))
                    return answer
                else:
                    raise TelegramNotifierServiceError(f'bad response data: "{response_json}" is not list')

    async def get_user_categories(self, user_tg_id: int) -> List[NotifyCategory]:
        if DEBUG_MODE:
            return [NotifyCategory(id=i, name=f'category number {i}') for i in range(1, 8, 3)]
        async with aiohttp.ClientSession() as session:
            async with session.get(notify_service_api_url + f'subscriptions/{user_tg_id}/categories') as response:
                if response.status != 200:
                    raise TelegramNotifierServiceError(f'response status is {response.status} (not 200)')
                response_json = await response.json()
                answer = []
                if isinstance(response_json, list):
                    for category_data in response_json:
                        answer.append(NotifyCategory(id=category_data['id'], name=category_data['name']))
                    return answer
                else:
                    raise TelegramNotifierServiceError(f'bad response data: "{response_json}" is not list')

    async def sub_user_to_category(self, user_tg_id: int, category_id: int) -> NoReturn:
        if DEBUG_MODE:
            return
        async with aiohttp.ClientSession() as session:
            async with session.post(notify_service_api_url +
                                    f'subscriptions/{user_tg_id}/categories/{category_id}/subscribe') as response:
                if response.status != 200:
                    raise TelegramNotifierServiceError(f'response status is {response.status} (not 200)')

    async def unsub_user_to_category(self, user_tg_id: int, category_id: int) -> NoReturn:
        if DEBUG_MODE:
            return
        async with aiohttp.ClientSession() as session:
            async with session.delete(notify_service_api_url +
                                      f'subscriptions/{user_tg_id}/categories/{category_id}/unsubscribe') as response:
                if response.status != 200:
                    raise TelegramNotifierServiceError(f'response status is {response.status} (not 200)')
