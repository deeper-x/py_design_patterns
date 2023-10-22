class Singleton(type):
    _instances: dict["Singleton", "Singleton"] = {}

    def __call__(self) -> "Singleton":
        if self not in self._instances:
            # instance = super().__call__()
            self._instances[self] = self

        return self._instances[self]

    def count_instances(self) -> int:
        return len(self._instances)
