import abc


class BaseTicketBuilder(abc.ABC):
    @abc.abstractmethod
    def build(self):
        pass
