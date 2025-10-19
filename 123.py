from typing import Callable

def process(func: Callable[[int, str], bool]):
    result = func(42, "hello")
    print(result)

# 定義一個符合 Callable 的函式
def my_callback(x: int, y: str) -> bool:
    print(f"收到參數：{x}, {y}")
    return x == 42 and y == "hello"

# 呼叫 process 並傳入函式
process(my_callback)

process(lambda x, y: x > 10 and "h" in y)