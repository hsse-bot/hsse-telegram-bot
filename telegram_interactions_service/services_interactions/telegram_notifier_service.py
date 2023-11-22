import aiohttp
from telegram_interactions_service.services_interactions.interactions_interfaces import \
    TelegramNotifierServiceInteractionInterface
from typing import NoReturn, List
from ..misc.dataclasses import User, NotifyCategory
from paths import notify_service_api_url
from ..exceptions import TelegramNotifierServiceError


class TelegramNotifierServiceInteraction(TelegramNotifierServiceInteractionInterface):

    async def notify(self, category: NotifyCategory, text: str) -> NoReturn:
        pass

    async def create_category(self, category: NotifyCategory) -> NoReturn:
        pass

    async def delete_category(self, category: NotifyCategory) -> NoReturn:
        pass

    async def get_all_categories(self) -> List[NotifyCategory]:
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
        pass

    async def sub_user_to_category(self, user: User, category: NotifyCategory) -> NoReturn:
        pass

    async def unsub_user_to_category(self, user: User, category: NotifyCategory) -> NoReturn:
        pass
