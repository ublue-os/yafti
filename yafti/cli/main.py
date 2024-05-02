import logging
import subprocess
import sys
from pprint import pprint
from typing import Annotated

import typer

import yafti.setup  # noqa
from yafti import __version__, log
from yafti.app import Yafti

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])
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
    ] = False,
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


# TODO: this needs to be cleaned up etc.
@app.command(name="fp-info")
def flatpak_info(fp_path: str = "/usr/bin/flatpak"):
    """
    Print flatpak info as json
    """
    results = __exec_cmd(fp_path)

    decoded_current = results.decode("utf-8").replace("current packages: ", "")
    headers = ["ref", "name", "runtime", "installation", "version", "options"]

    pkg_list = []
    for p in decoded_current.splitlines():
        turds = p.split("\t")

        with_headers = {headers[i]: t for i, t in enumerate(turds)}
        pkg_list.append(with_headers.copy())

    for i in pkg_list:
        cares = None
        opts = i.get("options")
        if "," in opts:
            chunks = opts.split(",")
            prefix = chunks[1].strip()
            if prefix == "current":
                prefix = "app"

            cares = f"{prefix}/{i.get('ref')}"

        if cares is not None:
            info = __exec_remote_info(fp_path, i.get("ref").strip())
            info["cares"] = cares
            pprint(info)


def __exec_cmd(fp_path: str) -> str:
    results = subprocess.run(
        [fp_path, "list", "--columns=ref,name,runtime,installation,version,options"],
        capture_output=True,
    )

    return results.stdout if results.returncode == 0 else ""


def __exec_remote_info(fp_path: str, ref: str):
    results = subprocess.run(
        [fp_path, "remote-info", "flathub", ref], capture_output=True
    )

    decoded_current = results.stdout.decode("utf-8").replace(ref, "")
    pkg_info = {}
    for p in decoded_current.splitlines():
        lines = p.strip().split("\t")
        for li in lines:
            if li:
                chunks = li.split(":")
                if len(chunks) == 2:
                    k, v = li.split(":")
                    pkg_info[k.strip().lower()] = v.strip().lower()
                else:
                    # likely a date, skipping can clean up later
                    continue

    return pkg_info


if __name__ == "__main__":
    typer.run(app)
