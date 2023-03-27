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


import math as ma
from fractions import Fraction

from generating_tasks_lib.polynom_generation import (PolynomGeneration,
                                                     PolynomGenerationSettings)


class Integral:
    def __init__(
        self,
        degree: int,
        roots: list,
        multiplicity: dict,
        low_border: str,
        up_border: str,
        variable: str = "x",
    ) -> None:
        self.degree: int = degree  # макс. степень полинома
        self.roots: list = roots  # введенные корни (вводить только с типом str!)
        self.variable: str = variable  # переменная
        self.multiplicity: dict = multiplicity
        self.polynom: str = ""
        self.low_border: str = low_border
        self.up_border: str = up_border
        self.integral: str = ""

    def integral_constructor(self) -> str:
        settings = PolynomGenerationSettings()
        tmp_roots: list = self.roots.copy()  # ToDo: поменять PolynomGeneration
        poly = PolynomGeneration(
            degree=self.degree,
            roots=tmp_roots,
            rational_coef=True,
            multiplicity=self.multiplicity,
            canon_view=False,
            variable=self.variable,
            settings=settings,
        )
        self.polynom = poly.polynom_constructor()
        self.latex()
        return self.integral

    def solve_one_root(self, root: str, root_deegre: int) -> float:
        return -1 / (
            (Fraction(self.up_border) - Fraction(root)) ** (root_deegre - 1)
        ) * 1 / (root_deegre - 1) - (
            -1
            / ((Fraction(self.low_border) - Fraction(root)) ** (root_deegre - 1))
            * 1
            / (root_deegre - 1)
        )

    def solve_log(self, root_1: str, root_2: str, A: float) -> float:
        return A * ma.log(
            abs(
                (Fraction(self.up_border) - Fraction(root_2))
                / (Fraction(self.up_border) - Fraction(root_1))
            )
        ) - A * ma.log(
            abs(
                (Fraction(self.low_border) - Fraction(root_2))
                / (Fraction(self.low_border) - Fraction(root_1))
            )
        )

    def calc_log(self, x: str) -> float:  # log(|(x-a)/(x-b)|)
        return ma.log(abs(Fraction(self.up_border) - Fraction(x))) - ma.log(
            abs(Fraction(self.low_border) - Fraction(x))
        )

    def solve(self) -> float | None:
        for root in self.roots:
            if Fraction(root) >= Fraction(self.low_border) and Fraction(
                root
            ) <= Fraction(self.up_border):
                return None

        if len(self.roots) == 1 and self.degree > 1:
            return self.solve_one_root(self.roots[0], self.degree)
        elif len(self.roots) == 1 and self.degree == 1:
            return self.calc_log(self.roots[0])

        if len(self.roots) == 2 and self.degree == 2:
            A: Fraction = 1 / (Fraction(self.roots[1]) - Fraction(self.roots[0]))
            if Fraction(self.roots[1]) > Fraction(self.roots[0]):
                return self.solve_log(self.roots[0], self.roots[1], A)
            else:
                return self.solve_log(self.roots[1], self.roots[0], A)
        else:
            if self.degree == 3:
                if self.multiplicity[self.roots[0]] == 1:
                    A: float = (
                        1 / (Fraction(self.roots[1]) - Fraction(self.roots[0])) ** 2
                    )
                    B: float = -A
                    C: float = 1 / (Fraction(self.roots[1]) - Fraction(self.roots[0]))
                    return (
                        A * self.calc_log(self.roots[0])
                        + B * self.calc_log(self.roots[1])
                        + C * self.solve_one_root(self.roots[1], 2)
                    )
                elif self.multiplicity[self.roots[1]] == 1:
                    A: float = (
                        1 / (Fraction(self.roots[0]) - Fraction(self.roots[1])) ** 2
                    )
                    B: float = -A
                    C: float = 1 / (Fraction(self.roots[0]) - Fraction(self.roots[1]))
                    return (
                        A * self.calc_log(self.roots[1])
                        + B * self.calc_log(self.roots[0])
                        + C * self.solve_one_root(self.roots[0], 2)
                    )
            elif self.degree == 4:
                if self.multiplicity[self.roots[0]] == 2:
                    root_1: Fraction = Fraction(self.roots[0])
                    root_2: Fraction = Fraction(self.roots[1])
                    A: float = -2 / (root_1 - root_2) ** 3
                    C: float = -A
                    B: float = 1 / (root_1 - root_2) ** 2
                    D: float = B
                    return (
                        A * self.calc_log(root_1)
                        + B * self.solve_one_root(root_1, 2)
                        + C * self.calc_log(root_2)
                        + D * self.solve_one_root(root_2, 2)
                    )
                elif self.multiplicity[self.roots[0]] == 1:
                    root_1: Fraction = Fraction(self.roots[0])
                    root_2: Fraction = Fraction(self.roots[1])
                    A: float = 1 / (root_1 - root_2) ** 3
                    B: float = -A
                    C: float = -1 / (root_1 - root_2) ** 2
                    D: float = -1 / (root_1 - root_2)
                    return (
                        A * self.calc_log(root_1)
                        + B * self.calc_log(root_2)
                        + C * self.solve_one_root(root_2, 2)
                        + D * self.solve_one_root(root_2, 3)
                    )
                elif self.multiplicity[self.roots[1]] == 1:
                    root_1: Fraction = Fraction(self.roots[1])
                    root_2: Fraction = Fraction(self.roots[0])
                    A: float = 1 / (root_1 - root_2) ** 3
                    B: float = -A
                    C: float = -1 / (root_1 - root_2) ** 2
                    D: float = -1 / (root_1 - root_2)
                    return (
                        A * self.calc_log(root_1)
                        + B * self.calc_log(root_2)
                        + C * self.solve_one_root(root_2, 2)
                        + D * self.solve_one_root(root_2, 3)
                    )

    def latex(self) -> None:  # функция преобразования в LaTeX формат
        self.polynom = self.polynom[2 : len(self.polynom) - 2]
        self.integral = (
            "\\int_{%s}^{%s}"
            % (
                str(self.latex_coef_modifier(self.low_border)),
                str(self.latex_coef_modifier(self.up_border)),
            )
            + " \\frac{%s}" % ("\\mathrm{d}{%s}" % (self.variable))
            + "{%s}" % (self.polynom)
        )

    @staticmethod
    def latex_coef_modifier(numb: str) -> str:
        if "/" in numb:
            numb = Fraction(numb)
        if type(numb) == Fraction:
            if numb.numerator < 0:
                if numb.denominator != 1:
                    return "-\\frac{%d}{%d}" % (numb.numerator * -1, numb.denominator)
                return "-\\{%d}" % (numb.numerator * -1)

            else:
                if numb.denominator != 1:
                    return "\\frac{%d}{%d}" % (numb.numerator, numb.denominator)
                return "\\{%d}" % (numb.numerator)
        return numb
