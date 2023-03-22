from pydantic import validate_arguments


class PackageScreenState:
    __slots__ = ["state"]

    @classmethod
    def from_dict(cls, data: dict) -> "PackageScreenState":
        self = cls()
        self.load(data)
        return self

    @validate_arguments
    def load(self, data: dict):
        for k, v in data.items():
            self.set(k, v)

    def __init__(self):
        self.state = {}

    @validate_arguments
    def remove(self, item: str) -> None:
        del self.state[item]

    @validate_arguments
    def on(self, item: str) -> None:
        self.set(item, True)

    @validate_arguments
    def off(self, item: str) -> None:
        self.set(item, False)

    @validate_arguments
    def toggle(self, item: str) -> bool:
        self.state[item] = not self.state[item]
        return self.get(item)

    @validate_arguments
    def set(self, item: str, state: bool) -> None:
        self.state[item] = state

    @validate_arguments
    def get_on(self, prefix: str = "") -> list[str]:
        return [
            item
            for item, value in self.state.items()
            if item.startswith(prefix) and value is True
        ]

    def keys(self) -> list[str]:
        return list(self.state.keys())

    @validate_arguments
    def get(self, item: str) -> bool:
        return self.state.get(item)


STATE = PackageScreenState()
