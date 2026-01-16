from typing import get_type_hints

def example(name: str, age: int = 20) -> str:
    return f"{name}-{age}"

type_hints = get_type_hints(example)
print(type_hints)
# 输出: {'name': <class 'str'>, 'age': <class 'int'>, 'return': <class 'str'>}