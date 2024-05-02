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
    - yafti.plugins.flatpak: com.github.marcoceppi.PackageName
    # Explicit install
    - yafti.plugins.flatpak:
        install: com.github.marcoceppi.PackageName
    # Install with options
    - yafti.plugins.flatpak:
        install:
          pkg: com.github.marcoceppi.PackageName
          update: true
          user: true
    # Remove a flatpak package
    - yafti.plugins.flatpak:
        remove: com.github.marcoceppi.PackageName
    # Remove with options
    - yafti.plugins.flatpak:
        remove:
          pkg: com.github.marcoceppi.PackageName
          force: true

Programmatic usage example:

  from yafti.plugins.flatpak import Flatpak
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
from typing import Any, List, Optional

from pydantic import BaseModel, ValidationError, root_validator

from yafti import log
from yafti.abc import YaftiPluginReturn
from yafti.plugins.run import Run

# TODO: refactor


class ApplicationDetail(BaseModel):
    """Flatpak application information"""

    id: str
    name: str
    version: str
    branch: str
    installation: str


class FlatpakListItem(BaseModel):
    """Flatpak application list results"""

    application: str
    ref: str
    name: str
    runtime: str
    installation: str
    options: str
    origin: str
    version: str


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

        @root_validator
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
        noninteractive: bool = False,
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
        cmd = [self.bin, "install", "-y"]
        cmd.extend(args)
        cmd.append(package)

        return await self.exec(" ".join(cmd))

    async def remove(
        self,
        package: str,
        user: bool = False,
        system: bool = True,
        force: bool = False,
        noninteractive: bool = False,
    ) -> YaftiPluginReturn:
        """Remove flatpak package on the host system"""
        args = self._parse_args(
            user=user, system=system, force=force, noninteractive=noninteractive
        )
        cmd = [self.bin, "remove", "-y"]
        cmd.extend(args)
        cmd.append(package)

        return await self.exec(" ".join(cmd))

    async def list(self) -> list[FlatpakListItem]:
        """
        list flatpak packages: https://flatpak.readthedocs.io/en

        supported columns:
            Name
            Description
            Application
            ID
            Version
            Branch
            Arch
            Origin
            Installation
            Ref
            Active
            commit
            Latest
            commit
            Installed
            size
            Options

        :return: list of Flatpack list

        """
        headers = [
            "application",
            "ref",
            "name",
            "runtime",
            "installation",
            "version",
            "options",
            "origin",
        ]
        cmd = [
            self.bin,
            "list",
            f" --columns={','.join(headers)}",
        ]

        results = await self.exec(" ".join(cmd))
        if results.returncode != 0:
            raise FlatpakException(
                f"{cmd} returned non-zero."
                f"return code: {results.returncode}"
                f"stdout: {results.stdout}"
                f"stderr: {results}"
            )

        decoded = results.stdout.decode("utf-8").replace("current packages: ", "")
        package_list = await self.__parse_package_list(headers, decoded)

        return package_list

    async def ls(self):
        """
        ls flatpak packages: https://flatpak.readthedocs.io/en

        supported columns:
            Name
            Description
            Application
            ID
            Version
            Branch
            Arch
            Origin
            Installation
            Ref
            Active
            commit
            Latest
            commit
            Installed
            size
            Options
        """
        headers = [
            "application",
            "ref",
            "name",
            "runtime",
            "installation",
            "version",
            "options",
        ]
        cmd = [
            self.bin,
            "list",
            f" --columns={','.join(headers)}",
        ]

        return await self.exec(" ".join(cmd))

    async def __parse_stdout(self, line: str):
        pass

    async def __parse_package_list(
        self, headers: List[str], response: str
    ) -> List[FlatpakListItem]:
        _package_list = []
        for p in response.splitlines():
            chunks = p.split("\t")
            with_headers = {headers[i]: t for i, t in enumerate(chunks)}

            _package_list.append(with_headers.copy())

        _results = None
        if isinstance(_package_list, list) and len(_package_list) > 0:
            _results = [FlatpakListItem(**p) for p in _package_list]
        else:
            log.info("No flat packages found")
            _package_list = []

        return _results

    def __call__(self, options) -> YaftiPluginReturn:
        try:
            params = self.validate(options)
        except ValidationError as e:
            log.error(f"plugin:flatpak:__call__ {str(e)}")
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

        # log.debug(**params.install)
        return YaftiPluginReturn(output=r.stdout, errors=r.stderr, code=r.returncode)

    # TODO: this should be the way...
    async def build_command(
        self, pkg: str, auto_approve: bool = False, force: bool = False, **kwargs
    ):
        """
        Build a flat pak package on the host system
        """
        # build rules
        # install = {
        #     "base": "install",
        # }
        #
        # user = kwargs.get("user", False)
        # system = kwargs.get("system", False)
        # noninteractive = kwargs.get("noninteractive", False)

        raise NotImplementedError
