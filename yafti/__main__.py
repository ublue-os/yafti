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

import sys

import yafti.setup  # noqa
from yafti.app import Yafti
from yafti.parser import parse


if len(sys.argv) > 1:
    cfg = sys.argv[1]  # TODO(MC): implement proper cli arguments

config = parse(cfg)
app = Yafti(config)
app.run(None)
