from abc import ABC, abstractmethod


class BaseTicketBuilder(ABC):
    @abstractmethod
    def build(self):
        pass
