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

/f

Run a command on the system

Configuration usage example:

  commands:
    pre:
    # Simple config
    - run: /usr/bin/whoami
    # Explicit full path plugin
    - yafti.plugin.run: /usr/bin/whoami
    # Run with parameters
    - run: /bin/ls -lah
    - run: ["/bin/ls", "-lah"]
    - run:
      - /bin/ls
      - "-lah"


Programmatic usage example:

  from yafti.plugin.run import Run
  r = Run()
  r.exec(["/usr/bin/whoami"])
  f.exec(pkg="com.github.marcoceppi.PackageName", reinstall=True)

  r("/usr/bin/whoami")
  r(cmd="/usr/bin/whoami")
  r(cmd=["/usr/bin/whoami"])

"""

import asyncio
import shlex
import subprocess

from pydantic import validate_arguments

from yafti import log
from yafti.abc import YaftiPlugin, YaftiPluginReturn


class Run(YaftiPlugin):
    async def exec(self, cmd: str) -> subprocess.CompletedProcess:
        log.debug("running command", cmd=cmd)
        proc = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await proc.communicate()

        log.info("command complete", cmd=cmd, code=proc.returncode)
        log.debug(
            "command complete",
            cmd=cmd,
            code=proc.returncode,
            stdout=stdout,
            stderr=stderr,
        )

        return subprocess.CompletedProcess(
            cmd, returncode=proc.returncode, stdout=stdout, stderr=stderr
        )

    @validate_arguments
    async def __call__(self, cmd: list[str] | str) -> YaftiPluginReturn:
        log.debug("run called", cmd=cmd)
        if isinstance(cmd, list):
            cmd = shlex.join(cmd)

        r = await self.exec(cmd)
        return YaftiPluginReturn(output=r.stdout, errors=r.stderr, code=r.returncode)
