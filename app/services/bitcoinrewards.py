import contextlib
import asyncio
from typing import NamedTuple

from telethon.tl.types import Message
from telethon.tl.types import TypeKeyboardButton

from .base import Base

from app import utils


class Coord(NamedTuple):
    row: int
    column: int


def get_coord(message: Message) -> Coord:
    r = 0
    c = 0

    for row in message.reply_markup.rows:  # type: ignore
        with contextlib.suppress(AttributeError):
            for button in row.buttons:
                if button.text == '🎯View ads':
                    return Coord(r, c)

                c += 1

            c = 0
        r += 1

    raise ValueError


class BitcoinRewards(Base):
    __bot_username__: str = '@BitcoinRewardsBot'

    async def run(self) -> None:
        await self.client.send_message(
            self.__bot_username__,
            '/start'
        )

        async for message in self.client.iter_messages(
                self.__bot_username__, limit=5):

            with contextlib.suppress(AttributeError, ValueError):
                coord = get_coord(message)
                break

        else:
            print(f'Got an error in {self} service')
            return

        while True:
            await utils.random_sleep(1, 2)

            print('clicking')
            await message.click(*coord)
            await asyncio.sleep(32)


