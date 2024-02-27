# SPDX-License-Identifier: Apache-2.0

import inspect
import logging

import gi
from rich.logging import RichHandler

_l = logging.getLogger("yafti")
__all__ = ["info", "warn", "error", "debug", "set_level"]


def setup():
    logging.basicConfig(
        level="DEBUG",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                show_path=True,
                show_time=False,
                rich_tracebacks=True,
                tracebacks_suppress=[gi, logging],
            )
        ],
    )


def _fmt(msg: dict) -> str:
    mod = inspect.getmodule(inspect.stack()[1][0])
    args = {"module": mod.__name__ if mod else ""} | msg
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
