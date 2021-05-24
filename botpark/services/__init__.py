from typing import Tuple
from typing import Type

from .base import Base
from .bitcoinrewards import BitcoinRewards
from .goto_website import LitecoinClick
from .goto_website import BCHClick
from .goto_website import DOGEClick


all_services: Tuple[Type[Base], ...] = (
    BitcoinRewards,
    LitecoinClick,
    BCHClick,
    DOGEClick,
)
