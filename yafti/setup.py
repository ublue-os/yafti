import logging

import gbulb
import gi
from rich.logging import RichHandler

gi.require_version("Adw", "1")
gi.require_version("Gtk", "4.0")
# gi.require_version('OSTree', '1.0')
# gi.require_version('Flatpak', '1.0')
gi.require_version("Rsvg", "2.0")
gi.require_version("GIRepository", "2.0")


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

gbulb.install(gtk=True)
