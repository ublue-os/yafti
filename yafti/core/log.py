# Copyright 2023 Marco Ceppi
# SPDX-License-Identifier: Apache-2.0

import logging
import inspect

__all__ = ["info", "warn", "error", "debug", "set_level"]

_l = logging.getLogger("yafti")


def _fmt(msg: dict) -> str:
    frame = inspect.stack()[-1]
    mod = inspect.getmodule(frame[0])
    args = {"module": mod.__name__} | msg
    return " ".join([f"{k}={v}" for k, v in args.items()])


def set_level(level):
    _l.setLevel(level)


def debug(message, **kwargs):
    _l.debug(f"{message} {_fmt(kwargs)}")


def info(message, **kwargs):
    _l.info(f"{message} {_fmt(kwargs)}")


def warn(message, *kwargs):
    _l.warn(f"{message} {_fmt(kwargs)}")


def error(message, *kwargs):
    _l.error(f"{message} {_fmt(kwargs)}")
