import random
from fractions import Fraction

from numpy import convolve

from generating_tasks_lib.polynom_generation import PolynomGenerationSettings


class PolynomGeneration:
    def __init__(
        self,
        degree: int,
        roots: list,
        rational_coefs: bool,
        multiplicity: dict,
        canon_view: bool,
        variable: str,
        settings: PolynomGenerationSettings,
    ):
        self._degree = degree  # макс. степень полинома
        self._roots = roots  # введенные корни (вводить только с типом str!)
        self._rational_coefs = rational_coefs  # наличие рациональных коэффициентов
        self._multiplicity = (
            multiplicity  # (x-a)^k отвечает за k {'корень'(str): степень(int)}
        )
        self._canon_view = canon_view  # канонический вид
        self._variable = (
            variable if variable == "x" else "(" + variable + ")"
        )  # переменная, по дефолту 'x'
        self._settings = settings

    def _full_random_generation(self) -> list:
        while True:
            polynom: list = []
            for coef in range(self._degree - len(self._roots) + 1):
                if not self._rational_coefs:
                    polynom.append(
                        random.randint(
                            self._settings.int_lowest, self._settings.int_highest
                        )
                    )
                else:
                    polynom.append(
                        Fraction(
                            random.randint(
                                self._settings.frac_lowest_num,
                                self._settings.frac_highest_num,
                            ),
                            random.randint(
                                self._settings.frac_lowest_den,
                                self._settings.frac_highest_den,
                            ),
                        )
                    )
            if 0 not in polynom:
                break
        return polynom

    def _roots_generation(self) -> list:
        polynom: list = []
        for root in self._roots:
            if "/" in root:
                root: Fraction = Fraction(root)
            else:
                root: int = int(root)
            polynom.append([1, -1 * root])
        return polynom

    def polynom_constructor(self) -> str:
        polynom_roots: list = self._roots_generation()
        self.multiplicity_setup(polynom_roots)
        if self._degree > len(self._roots):
            polynom = self._full_random_generation()
            if self._canon_view:
                for root in polynom_roots:
                    polynom = convolve(polynom, root)
                return self._latex(polynom, None)
            return self._latex(polynom, polynom_roots)
        elif self._degree == len(self._roots):
            if self._canon_view:
                polynom = [1]
                for root in polynom_roots:
                    polynom = convolve(root, polynom)
                return self._latex(polynom, None)
            return self._latex(None, polynom_roots)
        raise Exception(f"len(roots) > degree: {len(polynom_roots)} > {self._degree}")

    def _latex(self, polynom_first, polynom_second) -> str:
        latex_polynom: str = ""
        exceptions: list = []
        if polynom_second is not None:
            for coef in polynom_second:
                if coef not in exceptions:
                    if coef != 0:
                        numb = self._latex_coef_modifier(coef[1])
                        final_bracket: str = (
                            "(%s%s)" % (self._variable, numb)
                            if self._multiplicity[coef[1] * -1] == 1
                            else "(%s%s)^%d"
                            % (self._variable, numb, self._multiplicity[coef[1] * -1])
                        )
                        latex_polynom += final_bracket
                        exceptions.append(coef)
            if polynom_first is None:
                return f"\\[{latex_polynom}\\]"
            return f"\\[{latex_polynom}{self._latex_canon(polynom_first)}\\]"
        return f"\\[{self._latex_canon(polynom_first)}\\]"

    def _latex_canon(self, polynom: list) -> str:
        latex_string: str = ""
        if self._canon_view:
            degree_mem: int = self._degree
        else:
            degree_mem: int = self._degree - len(self._roots)
        current_degree: int = degree_mem
        for coef_orig in polynom:
            coef: str = self._latex_coef_modifier(coef_orig)
            if coef_orig != 0:
                if current_degree == degree_mem and current_degree != 1:
                    coef = self._plus_minus_one(coef)
                    if coef != "+":
                        if coef.startswith("+"):
                            latex_string += "%s%s^%d" % (
                                coef[1::],
                                self._variable,
                                current_degree,
                            )
                        else:
                            latex_string += "%s%s^%d" % (
                                coef,
                                self._variable,
                                current_degree,
                            )
                    else:
                        latex_string += "%s^%d" % (self._variable, current_degree)
                elif current_degree > 1:
                    coef = self._plus_minus_one(coef)
                    latex_string += "%s%s^%d" % (coef, self._variable, current_degree)
                elif current_degree == 1:
                    coef = self._plus_minus_one(coef)
                    if degree_mem == 1:
                        if coef.startswith("+"):
                            coef = coef[1::]
                    latex_string += "%s%s" % (coef, self._variable)
                elif current_degree == 0:
                    latex_string += "%s" % coef
            current_degree -= 1
        if self._canon_view:
            return latex_string
        else:
            return f"({latex_string})"

    def multiplicity_setup(self, polynom_roots: list) -> None:
        multip_dict: dict = {}
        for root in polynom_roots:
            multip_dict[root[1] * -1] = multip_dict.get(root[1] * -1, 0) + 1
        for value in multip_dict:
            if type(value) == Fraction:
                value_str: str = f"{value.numerator}/{value.denominator}"
            else:
                value_str: str = str(value)

            if self._multiplicity.get(value_str) is not None and self._multiplicity[value_str] > 1:
                multip_dict[value] = (
                    multip_dict.get(value, 0) + self._multiplicity[value_str] - 1
                )
        polynom_roots.clear()
        self._roots.clear()
        self._multiplicity = multip_dict
        for multi in self._multiplicity:
            for times in range(0, self._multiplicity[multi]):
                polynom_roots.append([1, multi * -1])
                if type(multi) == int:
                    self._roots.append(str(multi))
                elif type(multi) == Fraction:
                    self._roots.append(f"{multi.numerator}/{multi.denominator}")
        if self._degree < len(polynom_roots):
            raise Exception(f"degree error(degree < len(roots)): {self._degree} < {len(polynom_roots)}")

    @staticmethod
    def _latex_coef_modifier(numb) -> str:
        if type(numb) == Fraction:
            if numb.denominator == 1:
                numb = numb.numerator
            if numb.numerator < 0:
                return "-\\frac{%d}{%d}" % (numb.numerator * -1, numb.denominator)
            return "+\\frac{%d}{%d}" % (numb.numerator, numb.denominator)
        return "{:+}".format(numb)

    @staticmethod
    def _plus_minus_one(coef: str) -> str:
        if coef == "+1":
            return "+"
        elif coef == "-1":
            return "-"
        return coef
