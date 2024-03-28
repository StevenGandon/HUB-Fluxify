class Buffer(list):
    def __init__(self, prealocate_size: int) -> None:
        super().__init__(0x00 for _ in range(prealocate_size))

class UniqueBuffer(set):
    def __init__(self, prealocate_size: int) -> None:
        super().__init__(0x00 for _ in range(prealocate_size))

class StringBuffer(list):
    def __init__(self, string: str = '', prealocate_size: int = None) -> None:

        if prealocate_size is None:
            prealocate_size = len(string)

        size_range: list = range(prealocate_size)

        if (prealocate_size is not None):
            super().__init__(0x00 for _ in size_range)
            for i in range(prealocate_size):
                self[i] = string[i] if (i < len(string)) else ''

    def __str__(self) -> str:
        return (''.join(self))

    def __repr__(self) -> str:
        return (self.__str__())
