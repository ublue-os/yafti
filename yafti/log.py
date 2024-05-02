import logging

__all__ = ["info", "warn", "error", "debug", "set_level"]

_l = logging.getLogger("yafti")

# TODO: this generally needs an update to fix the _fmt issues and support async


def _fmt(msg: dict) -> str:
    return " ".join([f"{k}={v}" for k, v in msg.items()])


def set_level(level):
    _l.setLevel(level)


def debug(message, **kwargs):
    _l.debug(f"{message} {_fmt(kwargs)}")


def info(message, **kwargs):
    _l.info(f"{message} {_fmt(kwargs)}")


def warn(message, *kwargs):
    _l.warning(f"{message} {_fmt(kwargs)}")


def error(message, *kwargs):
    _l.error(f"{message} {_fmt(kwargs)}")
