from sys import path

lib_path = next(
    (
        x
        for x in path
        if "LANA\\generating_tasks_lib\\integral_and_series_generation" in x
    ),
    None,
).replace("LANA\\generating_tasks_lib\\integral_and_series_generation", "LANA")
path.append(lib_path)

import random



class Series:
    def __init__(self) -> None:
        # (ax-b)(ax-b+a)
        self.a: int = random.choice(
            [i - 10 for i in range(0, 10)] + [i for i in range(1, 11)]
        )
        self.b: int = random.choice(
            [i - 10 for i in range(0, 10)] + [i for i in range(1, 11)]
        )
        self.series: str = ""

    def series_constructor(self) -> str:
        self.series = (
            "\\sum_{%s}^{%s}" % ("x=1", "\\infty")
            + " \\frac{%s}" % ("1")
            + "{%s}"
            % (
                "("
                + str(self.a)
                + "n"
                + (" + " + str(self.b) if self.b > 0 else str(self.b))
                + ")"
                + "("
                + str(self.a)
                + "n"
                + (" + " + str(self.b + self.a) if self.b > 0 else str(self.b + self.a))
                + ")"
            )
        )
        return self.series

    def solve(self) -> float:
        A: float = 1 / self.a
        return A * (1 / (self.a + self.b))