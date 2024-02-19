# Copyright 2024 uBlue
# SPDX-License-Identifier: Apache-2.0

import logging
from typing import Annotated

import typer
import yaml

import yafti.setup  # noqa
from yafti.app import Yafti
from yafti.core import log
from yafti.core.config import Config


def run(
    config: typer.FileText = typer.Argument("/etc/yafti.yml"),
    debug: bool = False,
    force_run: Annotated[
        bool, typer.Option("-f", "--force", help="Ignore run mode and force run")
    ] = False,
):
    log.setup()
    log.set_level(logging.DEBUG if debug else logging.INFO)
    log.debug("starting up", config=config, debug=debug)

    config = Config.parse_obj(yaml.safe_load(config))
    app = Yafti(config)
    app.run(None, force_run=force_run)


def app():
    typer.run(run)


if __name__ == "__main__":
    app()
