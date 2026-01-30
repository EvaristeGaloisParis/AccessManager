from typing import Final
from  enum import StrEnum, auto

class AccessEnvironment(StrEnum):
    PROD: Final[str] = auto()
    UAT: Final[str] = auto()
    DEV: Final[str] = auto()
