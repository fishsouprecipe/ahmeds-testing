import abc

from telethon import TelegramClient


class Base(abc.ABC):
    client: TelegramClient

    @property
    @classmethod
    @abc.abstractmethod
    def __bot_username__(cls) -> str:
        ...

    def __init__(self, client: TelegramClient) -> None:
        self.client = client

    @abc.abstractmethod
    async def run(self) -> None:
        pass

    async def send_message(self, message: str) -> None:
        await self.client.send_message(self.__bot_username__, message)

    async def start_command(self) -> None:
        await self.send_message('/start')

    def __repr_name__(self) -> str:
        return type(self).__name__

    def __repr_values__(self) -> str:
        return ''

    def __repr__(self) -> str:
        return f'{self.__repr_name__()}({self.__repr_values__()})'
