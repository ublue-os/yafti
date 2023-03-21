import logging

import gbulb
import gi
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

gbulb.install(gtk=True)
