import asyncio
import re
from typing import Dict

from telethon import TelegramClient
from telethon.sessions import StringSession

from botpark import utils
from botpark import config
from botpark.services import all_services


def get_number() -> str:
    while True:
        number: str = input('Write phone number in format `+xxxyyyyyyyyy`: ')

        if re.match(r'^\+\d+$', number):
            return number

        print(f'Wrong phone number format {number}')

HELP_MESSAGE = """\

====================================================
                  botpark v 0.2
====================================================

botpark add - adds telegram account to sessions list
botpark remove - remove a number from the list
botpark list - lists all telegram account numbers
botpark run - run bots

"""


async def help_command(_: utils.StatesDict) -> None:
    print(HELP_MESSAGE)


async def remove_command(states: utils.StatesDict) -> None:
    phone_number = get_number()

    try:
        del states[phone_number]
        print(f'{phone_number} has bees successfully deleted')

    except KeyError:
        print(f'Phone number {phone_number} does not exist')


async def list_command(states: utils.StatesDict) -> None:
    if states:
        message = "All telegram accounts\n\n{}".format(",\n".join(
            map(lambda s: f'    {s}', states))
        )

        print(message)

    else:
        print('There are no accounts')


async def add_command(states: utils.StatesDict) -> None:
    phone_number = get_number()

    if phone_number in states:
        print(f'Phone number {phone_number} is already in states')

        return

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
    print(f'Starting up {phone_number}')

    async with client:
        services = [service_class(client) for service_class in all_services]

        try:
            await asyncio.gather(*(service.run() for service in services))

        finally:
            for service in services:
                setattr(service, 'cancelled', True)

            print(f'Ended {phone_number}')


async def run_command(states: utils.StatesDict) -> None:
    if not states:
        print(
            'No clients loaded! '
            'Use add command to add a new account instead'
        )

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

    await asyncio.gather(*(
        _run_client(phone_number, client)
        for phone_number, client in clients.items()
    ))

