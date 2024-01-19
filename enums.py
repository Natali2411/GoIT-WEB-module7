import enum


class GENDER(enum.Enum):
    MALE = "M"
    FEMALE = "F"


class GRADE(enum.Enum):
    A = {"code": "A", "value": 5}
    B = {"code": "B", "value": 4}
    C = {"code": "C", "value": 4}
    D = {"code": "D", "value": 3}
    F = {"code": "F", "value": 2}
    E = {"code": "E", "value": 2}


class SUBJECT(enum.Enum):
    MATH = "MATH"
    LITERATURE = "LITERATURE"
    HISTORY = "HISTORY"
    GEOGRAPHY = "GEOGRAPHY"
    MUSIC = "MUSIC"
    BIOLOGY = "BIOLOGY"
    PHYSICAL_TRAINING = "PHYSICAL_TRAINING"
    PAINTING = "PAINTING"


class CLI_ACTIONS(enum.Enum):
    CREATE = "create"
    UPDATE = "update"
    REMOVE = "remove"
    LIST = "list"
