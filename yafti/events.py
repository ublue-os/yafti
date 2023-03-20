"""
Copyright 2023 Marco Ceppi

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

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
