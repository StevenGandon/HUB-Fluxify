from .locals import *

class ConstantItem64(object):
    def __init__(self, item) -> None:
        self.type = ConstantItem64.get_type(item)
        self.item = item
        self.size_size = 8
        self.size = len(item) if self.type == CONSTANT_STRING else 8

    @staticmethod
    def get_type(item) -> int:
        if (isinstance(item, str)):
            return (CONSTANT_STRING)

        if (isinstance(item, (int, float, complex))):
            return (CONSTANT_INT)

        return (CONSTANT_UNKNOWN)

    def get_byte_codes(self) -> bytes:
        item = 0x00

        if (self.type == CONSTANT_STRING):
            item = self.item.encode()
        else:
            item = self.item.to_bytes(self.size, "big")

        return (bytes((self.type.to_bytes(1, "big") + self.size.to_bytes(self.size_size, "big") + item)))

class ConstantItem32(ConstantItem64):
    def __init__(self, item) -> None:
        self.type = ConstantItem32.get_type(item)
        self.item = item
        self.size_size = 4
        self.size = len(item) if self.type == CONSTANT_STRING else 4

def get_empty_constant() -> ConstantItem64:
    item: ConstantItem64 = ConstantItem64(None)

    item.size = 0
    return (0, item)

def add_constant_primitive(item, constant_class=ConstantItem64):
    if (item in STATIC_ADDR_TABLE):
        return STATIC_ADDR_TABLE[item][0]

    item_top = max(STATIC_ADDR_TABLE.values(), default=get_empty_constant(), key=lambda x: x[0])

    new_item = constant_class(item)
    new_ref = 0 if item_top[0] + item_top[1].size == 0 else item_top[0] + item_top[1].size + item_top[1].size_size + 1

    STATIC_ADDR_TABLE[item] = (
        new_ref,
        new_item
    )
    return (new_ref)
