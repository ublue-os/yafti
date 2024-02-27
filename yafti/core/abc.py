# SPDX-License-Identifier: Apache-2.0

import asyncio
from inspect import iscoroutinefunction
from typing import Any, Optional

from pydantic import BaseModel


class YaftiPlugin:
    pass


async def _show_screen(condition):
    from yafti.core.registry import PLUGINS

    plugin_name = list(condition.keys())[0]
    plugin = PLUGINS.get(plugin_name)
    result = await plugin(condition[plugin_name])
    return result.code == 0


class YaftiScreenConfig(BaseModel):
    condition: Optional[dict[str, str | dict]] = None


class YaftiScreen:
    active = False

    class Config(YaftiScreenConfig):
        pass

    @classmethod
    async def from_config(cls, cfg: Any):
        c = cls.Config.parse_obj(cfg)
        show = True
        if c.condition:
            show = await _show_screen(c.condition)
        if not show:
            return None

        return cls(**c.dict(exclude={"condition"}))

    def activate(self):
        self.active = True
        if hasattr(self, "on_activate"):
            if iscoroutinefunction(self.on_activate):
                asyncio.ensure_future(self.on_activate())
            else:
                self.on_activate()

    def deactivate(self):
        self.active = False
        if hasattr(self, "on_deactivate"):
            if iscoroutinefunction(self.on_deactivate):
                asyncio.ensure_future(self.on_deactivate())
            else:
                self.on_deactivate()


class YaftiPluginReturn(BaseModel):
    output: Optional[str | list[str]]
    errors: Optional[str | list[str]]
    code: int = 0
