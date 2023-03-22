def parse_packages(packages: dict | list) -> dict:
    output = {}

    if isinstance(packages, dict):
        for group, value in packages.items():
            output[f"group:{group}"] = True
            output.update(parse_packages(value["packages"]))
        return output

    for pkgcfg in packages:
        output.update({f"pkg:{package}": True for package in pkgcfg.values()})
    return output
