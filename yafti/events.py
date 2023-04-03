# Copyright 2023 Marco Ceppi
# SPDX-License-Identifier: Apache-2.0

from typing import Any

_listeners = {}


class EventException(Exception):
    """Event system encountered a problem"""


class EventAlreadyRegisteredError(EventException):
    """Event name already exists"""


class EventNotRegisteredError(EventException):
    """Event name does not exist"""


def register(event_name):
    if event_name in _listeners:
        raise EventAlreadyRegisteredError(
            "event is already registered", event=event_name
        )
    _listeners[event_name] = []


def on(event_name: str, fn: Any):
    if event_name not in _listeners:
        raise EventNotRegisteredError("event name not registered", event=event_name)
    if fn in _listeners[event_name]:
        return
    _listeners[event_name].insert(0, fn)


def detach(event_name: str, fn: Any):
    if event_name not in _listeners:
        raise EventNotRegisteredError("event name not registered", event=event_name)
    _listeners[event_name].remove(fn)


async def emit(event_name, *args, **kwargs):
    if event_name not in _listeners:
        raise EventNotRegisteredError("event name not registered", event=event_name)

    for fn in _listeners[event_name]:
        result = await fn(*args, **kwargs)
        if result is not False:
            break
