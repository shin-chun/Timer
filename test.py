from enum import Enum

class KeyState(Enum):
    IDLE = 0
    SELECT = 1
    LOCK = 2
    ACTIVE = 3
    SUB_ACTIVE1 = 4
    SUB_ACTIVE2 = 5
    SUB_ACTIVE3 = 6

print(KeyState.IDLE.value)
print(KeyState.SELECT)
print(KeyState.LOCK)