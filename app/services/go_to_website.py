import abc
import contextlib
import asyncio

from app import utils

from .base import Base

from .pw import get_page


JS_TO_EVALUATE = """
(function() {
    try {
        return document.URL;
    } catch (e) {
        return 'https://doge.click/';
    }
})()
"""

class GoToWebsiteBase(Base, abc.ABC):
    async def run(self) -> None:
        await self.start_command()

        while True:
            await self.send_message('🖥 Visit sites')
            await utils.random_sleep(2, 3)

            async for message in self.client.iter_messages(
                    self.__bot_username__, limit=5):


                with contextlib.suppress(AttributeError, ValueError):
                    coord = utils.get_coord(message, '🔎 Go to website')
                    break
            else:
                print(f'Got an error in {self} service')
                return

            button = message.buttons[coord.row][coord.column]

            async with get_page() as page:
                await page.goto(button.url)

                while True:
                    url = await page.evaluate(JS_TO_EVALUATE)

                    if '://doge.click' in url:
                        await asyncio.sleep(1)

                    else:
                        break

            await asyncio.sleep(10)


class LitecoinClick(GoToWebsiteBase):
    __bot_username__: str = '@Litecoin_click_bot'


class BCHClick(GoToWebsiteBase):
    __bot_username__: str = '@BCH_clickbot'


class DOGEClick(GoToWebsiteBase):
    __bot_username__: str = '@Dogecoin_click_bot'
