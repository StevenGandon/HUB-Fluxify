from .locals import *

class LabelItem64(object):
    def __init__(self, name, position) -> None:
        self.name = name
        self.position = position

class LabelItem32(LabelItem64):
    pass