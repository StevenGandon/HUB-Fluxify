from .locals import *

class LabelItem64(object):
    def __init__(self, name, position) -> None:
        self.name = name
        self.position = position

    def get_byte_codes(self) -> bytes:
        return (len(self.name).to_bytes(1, "big") + self.name.encode() + self.position.to_bytes(8, "big"))

class LabelItem32(LabelItem64):
    def get_byte_codes(self) -> bytes:
        return (len(self.name).to_bytes(1, "big") + self.name.encode() + self.position.to_bytes(4, "big"))
