from abc import ABC, abstractmethod
from typing import NoReturn


class BaseAttachmentsManager(ABC):
    @abstractmethod
    def get_content(self, attachment_id: int) -> bytes:
        pass

    @abstractmethod
    def delete(self, attachment_id: int) -> NoReturn:
        pass
    
    @abstractmethod
    def create(self, attachment_id: int, content: int) -> NoReturn:
        pass
