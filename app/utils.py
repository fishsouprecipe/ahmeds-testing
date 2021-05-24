import json
import asyncio
import random

from typing import Any
from typing import Dict
from pathlib import Path

import aiofiles


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


    await asyncio.sleep(random.random() * k)
