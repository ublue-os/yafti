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

import shlex
import subprocess
from typing import Any

from pydantic import BaseModel, ValidationError

from yafti.abc import YaftiPlugin, YaftiPluginReturn


class Run(YaftiPlugin):
    class Scheme(BaseModel):
        __root__: str

    def validate(self, options: Any):
        return self.Scheme.parse_obj(options)

    def exec(self, cmd: list[str]) -> subprocess.CompletedProcess:
        return subprocess.run(cmd, capture_output=True)

    def __call__(self, cmd: list[str] | str) -> YaftiPluginReturn:
        try:
            self.validate(cmd)
        except ValidationError as e:
            return YaftiPluginReturn(errors=str(e), code=1)

        if not isinstance(cmd, list):
            cmd = shlex.split(cmd)

        r = self.exec(cmd)
        return YaftiPluginReturn(output=r.stdout, errors=r.stderr, code=r.returncode)
