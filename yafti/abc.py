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

from typing import Any, Optional

from pydantic import BaseModel


class YaftiPlugin:
    pass


class YaftiScreen:
    active = False

    class Config(BaseModel):
        pass

    @classmethod
    def from_config(cls, cfg: Any):
        c = cls.Config.parse_obj(cfg)
        return cls(**c.dict())

    def activate(self):
        self.active = True
        if hasattr(self, "on_activate"):
            self.on_activate()

    def deactivate(self):
        self.active = False
        if hasattr(self, "on_deactivate"):
            self.on_deactivate()


class YaftiPluginReturn(BaseModel):
    output: Optional[str | list[str]]
    errors: Optional[str | list[str]]
    code: int = 0
