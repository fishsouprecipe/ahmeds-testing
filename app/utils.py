import json
import contextlib
import asyncio
import random

from typing import Any
from typing import TYPE_CHECKING
from typing import Dict
from typing import NamedTuple
from pathlib import Path

import aiofiles

if TYPE_CHECKING:
    from telethon.tl.types import Message


State = Dict[str, Any]
StatesDict = Dict[str, State]


async def load_states(states_file: Path) -> StatesDict:
    try:
        async with aiofiles.open(states_file) as f:
            content: str = await f.read()

            return json.loads(content)


    except FileNotFoundError:
        return {}


async def dump_states(states: StatesDict, states_file: Path) -> None:
    async with aiofiles.open(states_file, 'w') as f:
        content: str = json.dumps(states, indent=2)

        await f.write(content)


async def random_sleep(min: float, max: float) -> None:
    if max <= min:
        raise ValueError

    k = max - min

    await asyncio.sleep(random.random() * k + max)


class Coord(NamedTuple):
    row: int
    column: int


def get_coord(message: 'Message', button_text: str) -> Coord:
    r = 0
    c = 0

    for row in message.reply_markup.rows:  # type: ignore
        with contextlib.suppress(AttributeError):
            for button in row.buttons:
                if button.text == button_text:
                    return Coord(r, c)

                c += 1

            c = 0
        r += 1

    raise ValueError

