import abc
import time
import asyncio
import contextlib

from botpark import utils

from playwright.async_api import async_playwright

from .base import Base


async def goto_website(page, goto_url: str):
    await page.goto(goto_url)
    await asyncio.sleep(25)


class GoToWebsiteBase(Base, abc.ABC):
    async def run(self) -> None:
        await utils.random_sleep(2, 3)

        while True:
            if hasattr(self, 'cancelled'):
                return

            await self.send_message('🖥 Visit sites')

            for _ in range(4):
                async for message in self.client.iter_messages(
                    self.__bot_username__,
                    limit=5,
                ):

                    with contextlib.suppress(AttributeError, ValueError):
                        coord = utils.get_coord(message, '🔎 Go to website')
                        break

                else:
                    await utils.random_sleep(1, 3)

                    continue

                break

            else:
                print(f'Errored {self}')

                return

            button = message.buttons[coord.row][coord.column]

            started = time.monotonic()
            print('starting')
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()

                await goto_website(page, button.url)

            elapsed  = time.monotonic() - started
            print(elapsed)

            if elapsed < 10:
                await asyncio.sleep(10 - elapsed)


class LitecoinClick(GoToWebsiteBase):
    __bot_username__: str = '@Litecoin_click_bot'


class BCHClick(GoToWebsiteBase):
    __bot_username__: str = '@BCH_clickbot'


class DOGEClick(GoToWebsiteBase):
    __bot_username__: str = '@Dogecoin_click_bot'
