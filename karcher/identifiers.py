# -----------------------------------------------------------
# Copyright (c) 2023 Lauris BH
# SPDX-License-Identifier: MIT
# -----------------------------------------------------------

"""Compat layer for homeassistant."""
from enum import Enum, auto


class VacuumState(Enum):
    """Vacuum state enum.

    This offers a simplified API to the vacuum state.

    # TODO: the interpretation of simplified state should be done downstream.
    """

    Unknown = auto()
    Cleaning = auto()
    Returning = auto()
    Idle = auto()
    Docked = auto()
    Paused = auto()
    Error = auto()
