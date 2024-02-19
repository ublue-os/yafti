import logging

import gbulb
import gi
from rich.logging import RichHandler


gi.require_version("Adw", "1")
gi.require_version("Gtk", "4.0")

gbulb.install(gtk=True)
