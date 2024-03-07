"""
-- EPITECH PROJECT, 2024
-- Hub project
-- File description:
-- module init
"""

from .floff64 import (
    Floff64,
    Floff64Table
)
from .floff32 import (
    Floff32,
    Floff32Table
)
from .exceptions import (
    FloFFError,
    FloFFFilePermissionDenied,
    FloFFFileCompilerNameTooBig,
    FloFFFileInvalidArchitecture,
    FloFFFileInvalidMagic,
    FloFFFileNotFound,
    FloFFFileNumberOfTablesTooBig,
    FloFFFileStartingLabelAddressTooBig,
    FloFFFileTableContentTooBig
)
from .locals import *
