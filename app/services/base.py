import abc
import asyncio

from typing import Optional

from telethon import TelegramClient


class Base(abc.ABC):
    client: TelegramClient
    task: Optional[asyncio.Task]

    def __init__(self, client: TelegramClient) -> None:
        self.client = client
        self.task = None

    def start(self) -> None:
        if self.task is not None:
            raise RuntimeError(f'{self} is already runnig')

        self.task = asyncio.create_task(self.run())

    @abc.abstractmethod
    async def run(self) -> None:
        pass

    def stop(self) -> None:
        if self.task is None:
            raise RuntimeError(f'{self} is not runnig')

        self.task.cancel()
        self.task = None

    def __repr_name__(self) -> str:
        return type(self).__name__

    def __repr_values__(self) -> str:
        return ''

    def __repr__(self) -> str:
        return f'{self.__repr_name__()}({self.__repr_values__()})'
