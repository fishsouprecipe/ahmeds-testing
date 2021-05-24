import asyncio
import re
from typing import Dict
from typing import List

from telethon import TelegramClient
from telethon.sessions import StringSession

from app import utils
from app import config
from app.services import Base
from app.services import all_services

RE = re.compile(r'^\+\d+$')
MESSAGE = '''Add phone number in format
+yyyxxxxxxxx (not fixed width)
'''

async def add_command(states: utils.StatesDict) -> None:
    while True:
        phone_number: str = input(MESSAGE).strip()

        if not RE.match(phone_number):
            print(f'Wrong phone number format {phone_number}')

            continue

        if phone_number in states:
            print(f'Phone number {phone_number} is already in states')

        break

    client = TelegramClient(
        StringSession(),
        api_id=config.TELEGRAM_APP_ID,
        api_hash=config.TELEGRAM_APP_HASH,
    )

    await client.start(phone=lambda: phone_number)  # type: ignore

    session = client.session.save()

    if session:
        states[phone_number] = {'session': session}
        print(f'Phone number {phone_number} has been successfully added')

    else:
        print(f'Phone number {phone_number} has not been added')


async def _run_client(phone_number: str, client: TelegramClient) -> None:
    services: List[Base] = []

    print(f'Starting up {phone_number}')

    async with client:
        try:
            for service_class in all_services:
                service = service_class(client)
                service.start()
                services.append(service)

            while True:
                await asyncio.sleep(3600)

        finally:
            for service in services:
                service.stop()

            services = []

            print(f'Stopped {phone_number}')


async def run_command(states: utils.StatesDict) -> None:
    if not states:
        print('No clients loaded! Use add command to add a new account instead')
        return

    clients: Dict[str, TelegramClient] = {}

    for phone_number, state in states.items():
        session: str = state['session']

        client = TelegramClient(
            StringSession(session),
            api_id=config.TELEGRAM_APP_ID,
            api_hash=config.TELEGRAM_APP_HASH,
        )

        clients[phone_number] = client

    try:
        await asyncio.wait([
            asyncio.create_task(_run_client(phone_number, client))
            for phone_number, client in clients.items()
        ])

    finally:
        print('Done')
