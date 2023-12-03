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

    async def get_all_categories(self) -> List[NotifyCategory]:
        if DEBUG_MODE:
            return [NotifyCategory(id=i, name=f'category number {i}') for i in range(10)]
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

    async def get_user_categories(self, user: User) -> List[NotifyCategory]:
        if DEBUG_MODE:
            return [NotifyCategory(id=i, name=f'category number {i}') for i in range(5)]
        async with aiohttp.ClientSession() as session:
            async with session.get(notify_service_api_url + f'subscriptions/{user.tg_id}/categories') as response:
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

    async def sub_user_to_category(self, user: User, category: NotifyCategory) -> NoReturn:
        if DEBUG_MODE:
            return
        async with aiohttp.ClientSession() as session:
            async with session.post(notify_service_api_url +
                                    f'subscriptions/{user.tg_id}/categories/{category.id}/subscribe') as response:
                if response.status != 200:
                    raise TelegramNotifierServiceError(f'response status is {response.status} (not 200)')

    async def unsub_user_to_category(self, user: User, category: NotifyCategory) -> NoReturn:
        if DEBUG_MODE:
            return
        async with aiohttp.ClientSession() as session:
            async with session.delete(notify_service_api_url +
                                      f'subscriptions/{user.tg_id}/categories/{category.id}/unsubscribe') as response:
                if response.status != 200:
                    raise TelegramNotifierServiceError(f'response status is {response.status} (not 200)')
