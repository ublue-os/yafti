from pydantic import BaseModel


class PackageConfig(BaseModel):
    __root__: dict[str, str]


class PackageGroupConfigDetails(BaseModel):
    description: str
    default: bool = True
    packages: list[PackageConfig]


class PackageGroupConfig(BaseModel):
    __root__: dict[str, PackageGroupConfigDetails]
