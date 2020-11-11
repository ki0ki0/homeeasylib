from enum import Enum


def get_val(val):
    if issubclass(type(val), Enum):
        val = f'{val.name}({val})'
    return val
