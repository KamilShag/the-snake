import os
import sys
from random import randint
import random
x = 1


def f(a, b):
    return a + b


def g():
    y = 0
    z = 2
    q = 5
    l = [1, 2, 3, 4, 5]
    d = {"a": 1, "b": 2, "c": 3}
    if x == 1 and y != 2:
        return f(x, y)
    else:
        return None


class A:
    def m(self, a, b):
        self.result = a + b
        return self.result


def long_line():
    return "это очень длинная строка, которая специально написана так, что она превышает лимит в семьдесят девять символов PEP 8 и линтер на неё ругнётся"


def unused_var():
    result = 1
    return result


print(g(), A().m(2, 3))
