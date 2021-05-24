from typing import Tuple
from typing import Type

from .base import Base
from .bitcoinrewards import BitcoinRewards
from .go_to_website import LitecoinClick
from .go_to_website import BCHClick
from .go_to_website import DOGEClick


all_services: Tuple[Type[Base], ...] = (
    BitcoinRewards,
    LitecoinClick,
    BCHClick,
    DOGEClick,
)
