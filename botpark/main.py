import asyncio
import contextlib
import argparse
from typing import Sequence
from typing import Optional
from pathlib import Path

from botpark import defaults
from botpark import utils
from botpark.commands import add_command
from botpark.commands import list_command
from botpark.commands import remove_command
from botpark.commands import run_command
from botpark.commands import help_command


async def amain(argv: Optional[Sequence[str]] = None) -> None:
    parser = argparse.ArgumentParser(prog='ahmeds-testing')
    parser.add_argument('--states-file',
        type=Path,
        default=defaults.STATE_FILE,
    )
    parser.set_defaults(func=help_command)

    subparsers = parser.add_subparsers()
    add_parser = subparsers.add_parser('add')
    add_parser.set_defaults(func=add_command)

    run_parser = subparsers.add_parser('run')
    run_parser.set_defaults(func=run_command)

    list_parser = subparsers.add_parser('list')
    list_parser.set_defaults(func=list_command)

    remove_parser = subparsers.add_parser('remove')
    remove_parser.set_defaults(func=remove_command)

    args: argparse.Namespace = parser.parse_args(argv)

    states: utils.StatesDict = await utils.load_states(args.states_file)

    try:
        await args.func(states)

    finally:
        await utils.dump_states(states, args.states_file)


def main() -> None:
    with contextlib.suppress(Exception):
        asyncio.run(amain())

    print('\rGoodbye')
