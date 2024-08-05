from pydantic import RootModel, BaseModel


PackageConfig = RootModel[dict[str, str | dict]]


class PackageGroupConfigDetails(BaseModel):
    description: str
    default: bool = True
    packages: list[PackageConfig]


PackageGroupConfig = RootModel[dict[str, PackageGroupConfigDetails]]
