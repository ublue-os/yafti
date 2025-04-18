import asyncio
import logging

import gi
from gi.events import GLibEventLoopPolicy
from rich.logging import RichHandler

logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[
        RichHandler(
            show_path=False,
            show_time=False,
            rich_tracebacks=True,
            tracebacks_suppress=[gi, logging],
        )
    ],
)

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

asyncio.set_event_loop_policy(GLibEventLoopPolicy())
