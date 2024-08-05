from pydantic import validate_call


class PackageScreenState:
    __slots__ = ["state"]

    def __new__(cls, id: str):
        if not hasattr(cls, "instances"):
            cls.instances = {}
        if id not in cls.instances:
            cls.instances[id] = super(PackageScreenState, cls).__new__(cls)
        return cls.instances[id]

    def __init__(self, id: str):
        self.state = {}

    @validate_call
    def load(self, data: dict):
        for k, v in data.items():
            self.set(k, v)

    @validate_call
    def remove(self, item: str) -> None:
        del self.state[item]

    @validate_call
    def on(self, item: str) -> None:
        self.set(item, True)

    @validate_call
    def off(self, item: str) -> None:
        self.set(item, False)

    @validate_call
    def toggle(self, item: str) -> bool:
        self.state[item] = not self.state[item]
        return self.get(item)

    @validate_call
    def set(self, item: str, state: bool) -> None:
        self.state[item] = state

    @validate_call
    def get_on(self, prefix: str = "") -> list[str]:
        return [
            item
            for item, value in self.state.items()
            if item.startswith(prefix) and value is True
        ]

    def keys(self) -> list[str]:
        return list(self.state.keys())

    @validate_call
    def get(self, item: str) -> bool:
        return self.state.get(item)
