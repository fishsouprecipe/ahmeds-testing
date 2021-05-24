from typing import Tuple
from typing import Type

from .base import Base
from .bitcoinrewards import BitcoinRewards


all_services: Tuple[Type[Base], ...] = (
    BitcoinRewards,
)
