from enum import IntEnum, auto


class RNATypeCoarse(IntEnum):
    abstain = -1
    tRNA = 0
    rRNA = 1
    other = 2


class RNAType(IntEnum):
    abstain = -1
    SO_0000253 = auto()  # tRNA
    SO_0000655 = auto()
    SO_0000274 = auto()  # snRNA
    SO_0000275 = auto()  # snoRNA
    SO_0000404 = auto()  # vault_RNA
