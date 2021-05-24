import asyncio
import contextlib

from typing import Optional
from typing import Any

from playwright.async_api import async_playwright
from playwright.async_api._context_manager import PlaywrightContextManager
from playwright.async_api._context_manager import AsyncPlaywright


MAX_PAGES = 12

sem = asyncio.Semaphore(MAX_PAGES)
lock = asyncio.Lock()
pw: Optional[AsyncPlaywright] = None
pw_manager: Optional[PlaywrightContextManager] = None
browser: Any = None


@contextlib.asynccontextmanager
async def get_page():
    async with sem:
        page = await browser.new_page()

        try:
            yield page

        finally:
            await page.close()


async def init():
    global pw
    global pw_manager
    global browser

    async with lock:
        if pw_manager is None:
            pw_manager = async_playwright()

        if pw is None:
            pw = await pw_manager.__aenter__()

        if browser is None:
            browser = await pw.chromium.launch(headless=True)


async def stop():
    try:
        pass

    finally:
        async with lock:
            if browser:
                await browser.close()

            if pw_manager:
                await pw_manager.__aexit__()
