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


class NoParentFound(Exception):
    """No parent matched"""


def find_parent(obj, cls=None):
    """Traverse to the parent of a GTK4 component

    Args:
        obj: A GTK4 derived component
        cls: Parent component to find

    Returns:
        The instance of the parent component

    Raises:
        NoParentFound: if a cls is passed and all parents are traversed without a match
    """

    p = obj.get_parent()
    if cls:
        if isinstance(p, cls):
            return p
        if p is None:
            raise NoParentFound(f"no matching parent found for {cls}")

    if p is None:
        return obj

    return find_parent(p, cls)
