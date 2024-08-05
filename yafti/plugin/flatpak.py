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

\f

Install, remove, list, and manage flatpaks

Configuration usage example:

  commands:
    pre:
    # Install a Flatpak package
    - yafti.plugin.flatpak: com.github.marcoceppi.PackageName
    # Explicit install
    - yafti.plugin.flatpak:
        install: com.github.marcoceppi.PackageName
    # Install with options
    - yafti.plugin.flatpak:
        install:
          pkg: com.github.marcoceppi.PackageName
          update: true
          user: true
    # Remove a flatpak package
    - yafti.plugin.flatpak:
        remove: com.github.marcoceppi.PackageName
    # Remove with options
    - yafti.plugin.flatpak:
        remove:
          pkg: com.github.marcoceppi.PackageName
          force: true

Programmatic usage example:

  from yafti.plugin.flatpak import Flatpak
  f = Flatpak()
  f.install("com.github.marcoceppi.PackageName")
  f.install(pkg="com.github.marcoceppi.PackageName", reinstall=True)

  f("com.github.marcoceppi.PackageName")
  f(install="com.github.marcoceppi.PackageName")
  f(install={"pkg": "com.github.marcoceppi.PackageName", "reinstall": True})

  f.remove("com.github.marcoceppi.PackageName")
  f.remove(pkg="com.github.marcoceppi.PackageName", force=True)

  f(remove="com.github.marcoceppi.PackageName")
  f(remove={"pkg": "com.github.marcoceppi.PackageName", "force": True})
"""

import asyncio
from typing import Any, Optional

from pydantic import BaseModel, ValidationError, field_validator

from yafti.abc import YaftiPluginReturn
from yafti.plugin.run import Run


class ApplicationDetail(BaseModel):
    """Flatpak application information"""

    id: str
    name: str
    version: str
    branch: str
    installation: str


class FlatpakException(Exception):
    """Flatpak binary encountered a problem"""


class FlatpakInstallError(FlatpakException):
    """Flatpak package install failed"""


class FlatpakRemoveError(FlatpakException):
    """Flatpak package removal failed"""


class Flatpak(Run):
    """
    Install, remove, list, and manage flatpaks

    Attributes:
        bin: The full POSIX path to the flatpak binary on disk
    """

    class Scheme(BaseModel):
        """Flatpak plugin configuration validation"""

        install: Optional[str | dict] = None
        remove: Optional[str | dict] = None

        @field_validator("install", "remove")
        def must_have_atleast_one(cls, values):
            """Validate one, and only one, key is passed

            Returns:
                A dict of the already parsed values from Pydantic

            Raises:
                ValueError: A violation of the validation rule.
            """
            if values.get("install") is None and values.get("remove") is None:
                raise ValueError("Either install or remove is required")
            if values.get("install") is not None and values.get("remove") is not None:
                raise ValueError("Only a single install or remove can be passed")
            return values

    def __init__(self):
        """Verify that flatpak binary exists on the host machine"""
        self.bin = "/usr/bin/flatpak"

    def validate(self, options: Any) -> Scheme:
        """Sanitize and validate inputs

        Args:
            options: Plugin arguments to be validated and sanitized

        Returns:
            An object of the parsed input options

        Raises:
            ValidationError: Input could not be sanitized and did not conform to
                             validation rules
        """
        if isinstance(options, str):
            options = {"install": options}

        return self.Scheme.parse_obj(options)

    def _parse_args(self, **kwargs):
        """Map a series of boolean keyword arguments to command-line flags"""
        arg_map = {"update": "or-update"}

        return [f"--{arg_map.get(k, k)}" for k, v in kwargs.items() if v is True]

    async def install(
        self,
        package: str,
        user: bool = True,
        system: bool = False,
        assumeyes: bool = True,
        reinstall: bool = False,
        noninteractive: bool = True,
        update: bool = True,
    ) -> YaftiPluginReturn:
        """Install flatpak package on the host system

        Args:
          package: Name of the flatpak package to install
          user: Install on the user installation
          system: Install on the system-wide installation
          assumeyes:

        Returns:
          An object containing the stdout and stderr from the flatpak command

        Raises:
          FlatpakInstallError: An error occurred trying to install the Flatpak
        """
        args = self._parse_args(
            user=user,
            system=system,
            assumeyes=assumeyes,
            reinstall=reinstall,
            update=update,
            noninteractive=noninteractive,
        )
        cmd = [self.bin, "install"]
        cmd.extend(args)
        cmd.append(package)
        return await self.exec(" ".join(cmd))

    async def remove(
        self,
        package: str,
        user: bool = False,
        system: bool = True,
        force: bool = False,
        noninteractive: bool = True,
    ) -> YaftiPluginReturn:
        """Remove flatpak package on the host system"""
        args = self._parse_args(
            user=user, system=system, force=force, noninteractive=noninteractive
        )
        cmd = [self.bin, "remove"]
        cmd.extend(args)
        cmd.append(package)
        return self.exec(cmd)

    def ls(self) -> list[ApplicationDetail]:
        pass

    def __call__(self, options) -> YaftiPluginReturn:
        try:
            params = self.validate(options)
        except ValidationError as e:
            return YaftiPluginReturn(errors=str(e), code=1)

        # TODO: when a string is passed, make sure it maps to the "pkg" key.
        if params.install:
            if isinstance(params.install, str):
                params.install = {"package": params.install}
            r = asyncio.ensure_future(self.install(**params.install))
        else:
            if isinstance(params.remove, str):
                params.remove = {"package": params.remove}
            r = asyncio.ensure_future(self.remove(**params.install))
        return YaftiPluginReturn(output=r.stdout, errors=r.stderr, code=r.returncode)
