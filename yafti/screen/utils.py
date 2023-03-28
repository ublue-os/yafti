# Copyright 2023 Marco Ceppi
# SPDX-License-Identifier: Apache-2.0

from typing import Any


class NoParentFound(Exception):
    """No parent matched"""


def find_parent(obj: Any, cls: Any = None):
    """Traverse to the parent of a GTK4 component

    Args:
        obj: A GTK4 derived component
        cls: Parent component to find

    Returns:
        The instance of the parent component

    Raises:
        NoParentFound: if a cls is passed and all parents are traversed without a match
    """

    p = obj.get_parent()
    if cls:
        if isinstance(p, cls):
            return p
        if p is None:
            raise NoParentFound(f"no matching parent found for {cls}")

    if p is None:
        return obj

    return find_parent(p, cls)
