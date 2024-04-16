import csv
import json
from hashlib import sha256
from io import StringIO
from typing import Any, List


def generate_fingerprint(obj: Any):
    return sha256(json.dumps(obj).encode()).hexdigest()


def parse_packages(packages: dict | list) -> dict:
    output = {}

    if isinstance(packages, dict):
        for group, value in packages.items():
            output[f"group:{group}"] = True
            output.update(parse_packages(value["packages"]))

        return output

    for pkgcfg in packages:
        for package in pkgcfg.values():
            if isinstance(package, dict):
                package = json.dumps(package)
            output[f"pkg:{package}"] = True

    return output


def _format_complex(record: dict) -> dict:
    # don't want to get rid of non-csv values, so we will
    #  simply write them as a JSON string instead

    json_opts = (",", ":")
    cast_types = (list, tuple, dict)

    return {
        k: (v if not isinstance(v, cast_types) else json.dumps(v, separators=json_opts))
        for k, v in record.items()
    }


def to_json(records: List[dict]) -> str:
    return json.dumps(records, indent=4)


def formatter(data: List[dict], output_type: str) -> str:
    formats = {"json": to_json, "csv": to_csv}

    return formats[output_type](data)


def fs(data: str, filename: str) -> None:
    with open(filename, "w") as f:
        f.write(data)


def to_csv(records: List[dict]) -> str:
    if not records:
        return ""

    defaults = {
        "delimiter": ",",
        "quoting": csv.QUOTE_MINIMAL,
        "dialect": "excel",
        "lineterminator": "\n",
    }

    handler = StringIO()
    header = records[0].keys()
    writer = csv.DictWriter(handler, fieldnames=header, **defaults)
    writer.writeheader()
    for record in records:
        writer.writerow(_format_complex(record))

    return handler.getvalue()


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
