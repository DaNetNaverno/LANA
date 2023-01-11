from random import randint


class SumTaskOptions:
    def __init__(self, min: int, max: int, amount: int):
        self.min = min
        self.max = max
        self.amount = amount


def generate_sum_task(options: SumTaskOptions) -> (str, str):
    res = 0
    latex = ""
    for i in range(options.amount):
        term = randint(options.min, options.max)
        res += term
        if i == 0:
            latex = str(term)
        else:
            latex += f" + {term}"
    return latex, res
