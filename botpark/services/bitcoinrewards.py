import contextlib
import asyncio

from .base import Base

from botpark import utils


class BitcoinRewards(Base):
    __bot_username__: str = '@BitcoinRewardsBot'

    async def run(self) -> None:
        await self.start_command()
        await utils.random_sleep(3, 4)

        async for message in self.client.iter_messages(
                self.__bot_username__, limit=5):

            with contextlib.suppress(AttributeError, ValueError):
                coord = utils.get_coord(message, '🎯View ads')
                break

        else:
            print(f'Got an error in {self} service')
            return

        while True:
            await utils.random_sleep(1, 2)
            await message.click(*coord)
            await asyncio.sleep(32)


