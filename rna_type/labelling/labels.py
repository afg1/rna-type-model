from enum import IntEnum, auto


class RNATypeCoarse(IntEnum):
    abstain = -1
    tRNA = 0
    rRNA = 1
    other = 2


class RNAType(IntEnum):
    abstain = -1
    SO_0000655 = auto()
