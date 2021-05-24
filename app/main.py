import argparse
from typing import Sequence
from typing import Optional
from pathlib import Path

from app import config
from app import utils
from app.commands import add_command
from app.commands import run_command


async def main(argv: Optional[Sequence[str]] = None) -> None:
    parser = argparse.ArgumentParser(prog='ahmeds-testing')
    parser.add_argument(
        '--states-file',
        type=Path,
        default=config.PROJECT_DIR / 'states.json'
    )

    subparsers = parser.add_subparsers()
    add_parser = subparsers.add_parser('add')
    add_parser.set_defaults(func=add_command)

    run_parser = subparsers.add_parser('run')
    run_parser.set_defaults(func=run_command)

    args: argparse.Namespace = parser.parse_args(argv)

    states: utils.StatesDict = await utils.load_states(args.states_file)

    try:
        await args.func(states)

    finally:
        await utils.dump_states(states, args.states_file)
