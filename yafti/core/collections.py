import asyncio
import logging
import pprint
from functools import partial
from typing import Dict, List

from gi.repository import Adw, Gdk

from yafti import events
from yafti.registry import PLUGINS, SCREENS


class CollectionsMapper:
    def __init__(self, **kwargs):
        self.title: str
        self.tasks: Dict

        super().__init__(self, **kwargs)

    @classmethod
    def convert_to_collection(self, **kwargs):
        return CollectionsMapper(**kwargs)

    @classmethod
    def from_collection(cls, collections: List):
        return {}
