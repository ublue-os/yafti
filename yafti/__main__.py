# Copyright 2023 Marco Ceppi
# SPDX-License-Identifier: Apache-2.0

import logging

import typer
import yaml

import yafti.setup  # noqa
from yafti import log
from yafti.app import Yafti
from yafti.parser import Config


def run(config: typer.FileText = typer.Argument("/etc/yafti.yml"), debug: bool = False):
    log.set_level(logging.DEBUG if debug else logging.INFO)
    log.debug("starting up", config=config, debug=debug)
    config = Config.parse_obj(yaml.safe_load(config))
    app = Yafti(config)
    app.run(None)


def app():
    typer.run(run)


if __name__ == "__main__":
    app()
