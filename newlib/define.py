class Module:
    def __init__(self, name: str, content: dict[str:callable]):
        self.name = name
        self.content = content