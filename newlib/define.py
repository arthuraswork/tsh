class Module:
    def __init__(self, name: str, content: dict[str:callable]):
        self.name = name
        self.content = content

    def __call__(self, function: str, text: str):
        func = self.content.get(function)
        if func:
            result = func(text)
            if result:
                return result
        return ''