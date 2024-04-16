import logging
import sys
from typing import Annotated

import typer
import yaml

from yafti import __version__
import yafti.setup  # noqa
from yafti import log
from yafti.app import Yafti
from yafti.parser import Config


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


app = typer.Typer(context_settings=CONTEXT_SETTINGS, help="yafti command line tool")


@app.callback()
def callback(ctx: typer.Context) -> None:
    """callback"""
    pass


@app.command()
def version(ctx: typer.Context) -> None:
    """
    Show yafti version
    """
    typer.echo(f"Platform:         {sys.platform}")
    typer.secho(f"Python Version:   {sys.version}")
    typer.secho(f"Yafti Version:    {__version__}")


@app.command(name="start")
def start(
        config: typer.FileText = typer.Argument("/etc/yafti.yml"),
        debug: bool = False,
        force_run: Annotated[
            bool, typer.Option("-f", "--force", help="Ignore run mode and force run")
        ] = False
) -> None:
    """
    Run yafti using the config file
    """
    log.set_level(logging.DEBUG if debug else logging.INFO)
    log.debug("starting up", config=config, debug=debug)
    try:
        attempt = Yafti(config)
        attempt.run(None, force_run=force_run)
    except Exception as e:
        log.error("unable to run yafti: ", e)
        sys.exit(1)


if __name__ == '__main__':
    typer.run(app)
