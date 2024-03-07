"""
-- EPITECH PROJECT, 2024
-- Hub project
-- File description:
-- module init
"""

from .floff import (
    Floff64,
    Floff64Table
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
