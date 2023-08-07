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

import logging
from typing import Annotated

import typer
import yaml

import yafti.setup  # noqa
from yafti import log
from yafti.app import Yafti
from yafti.parser import Config


def run(
    config: typer.FileText = typer.Argument("/etc/yafti.yml"),
    debug: bool = False,
    force_run: Annotated[
        bool, typer.Option("-f", "--force", help="Ignore run mode and force run")
    ] = False,
):
    log.set_level(logging.DEBUG if debug else logging.INFO)
    log.debug("starting up", config=config, debug=debug)
    config = Config.parse_obj(yaml.safe_load(config))
    app = Yafti(config)
    app.run(None, force_run=force_run)


def app():
    typer.run(run)


if __name__ == "__main__":
    app()
