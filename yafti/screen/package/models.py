from pydantic import BaseModel, RootModel


class PackageConfig(RootModel):
    root: dict[str, str | dict]


class PackageGroupConfigDetails(BaseModel):
    description: str
    default: bool = True
    packages: list[PackageConfig]


class PackageGroupConfig(RootModel):
    root: dict[str, PackageGroupConfigDetails]
