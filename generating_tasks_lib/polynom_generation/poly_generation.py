import random
from fractions import Fraction

import numpy
from numpy import convolve, ndarray
from poly_settings import PolynomGenerationSettings
# from generating_tasks_lib.polynom_generation.poly_settings import (
#      PolynomGenerationSettings,
# )

class PolynomGeneration:
    """
    :param _degree: максимальная степень полинома
    :type _degree: int`

    :param _roots: список корней полинома (только str)
    :type _roots: list[str]

    :param _rational_coefs: наличие рациональных коэффикиентов при генерации
    :type _rational_coefs: bool

    :param _multiplicity: при наличии конструкции (x-a)^k отвечает за k (оформление: {'корень'(str): степень(int)})
    :type _multiplicity: dict

    :param _canon_view: канонический вид полинома (да/нет)
    :type _canon_view: bool

    :param _variable: обозначение переменной
    :type _variable: str

    :param _settings: настройки генерации коэффикиентов
    :type _settings: PolynomGenerationSettings

    Настройки по умолчанию: отсутствие рациональных коэффициентов, без повторяющихся корней, неканонический вид, переменная 'x'
    Минимальный набор для ввода: степень, как минимум один корень
    """

    def __init__(
            self,
            degree: int,
            multiplicity: dict[str | int, int],
            settings: PolynomGenerationSettings = PolynomGenerationSettings(),
            canon_view: bool = True,
            rational_coefs: bool = False,
            variable: str = 'x',
    ):
        self._degree = degree
        self._rational_coefs = rational_coefs
        self._multiplicity = multiplicity
        self._canon_view = canon_view
        self._variable = (
            variable if len(variable) == 1 else "(" + variable + ")"
        )
        self._settings = settings
        self._roots = []

    def _full_random_generation(self) -> list[int | Fraction]:
        """
        Метод генерирует коэффициенты для полинома, который возникает в случае,
        если есть разница между максимальной степенью "полного" полинома
        и количеством введенных корней

        :param polynom: список сгенерированных коэффициентов полинома
        :type polynom: list[int|Fraction]

        :return: список сгенерированных коэффициентов полинома
        :rtype: list[int|Fraction]
        """
        if len(self._multiplicity) == 0:
            raise Exception("Необходимо ввести как минимум один корень")
        while True:
            polynom: list[int | Fraction] = []
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

    def polynom_constructor(self) -> str:
        """
        !!! Основной метод, который необходимо вызывать для генерации полинома !!!
        Главным образом объединяет работу большинства методов класса
        В дополнение проверяет, имеется ли непреднамеренное совпадение корней и преображает полином в канонический вид
        в случае необходимости (на уровне массива)

        :param polynom_roots: список списков, каждое значение которого будет представлять из себя одну "скобку" полинома
        :type polynom_roots: list[list[int|Fraction]]

        :param polynom: список сгенерированных коэффициентов полинома
                        [подробности в _full_random_generation()]
        :type polynom: list[int|Fraction]

        :param polynom_check: корни сгенерированного в _full_random_generation() полинома
        :type polynom_check: ndarray[numpy.complex128|numpy.float64]

        :param polynom_check2: преобразованные в тип float корни полинома, введенные пользователем
        :type polynom_check: ndarray[numpy.complex128|numpy.float64]

        :param polynom_arr: массив, содержащий коэффициенты канонического полинома
        :type polynom_arr: ndarray[int|Fraction]

        :return: сгенерированный полином в латех формате (подробности в _latex())
        :rtype: str
        """
        polynom_roots: list[list[int | Fraction]] = self._roots_setup()
        polynom_arr: ndarray[int | Fraction] = numpy.array([1], dtype=numpy.int64)
        if self._degree > len(self._roots):
            while True:
                polynom: list[int | Fraction] = self._full_random_generation()
                polynom_check: ndarray[numpy.complex128 | numpy.float64 | numpy.int64] = numpy.roots(polynom)
                polynom_check2: ndarray[numpy.complex128 | numpy.float64 | numpy.int64] = numpy.array([], dtype=numpy.float64)
                for rooot in self._roots:
                    polynom_check2 = numpy.append(polynom_check2, eval('/'.join(map(str,map(float,rooot.split("/"))))))
                if not (set(polynom_check) & set(polynom_check2)):
                    break
            if self._canon_view:
                polynom_arr = convolve(polynom_arr, polynom)
                for root in polynom_roots:
                    polynom_arr = convolve(polynom_arr, root)
                return self._latex(polynom_arr, None)
            return self._latex(polynom, polynom_roots)
        elif self._degree == len(self._roots):
            if self._canon_view:
                polynom_arr = numpy.array([1], dtype=numpy.int64)
                for root in polynom_roots:
                    polynom_arr = convolve(root, polynom_arr)
                return self._latex(polynom_arr, None)
            return self._latex(None, polynom_roots)
        raise Exception(f"len(roots) > degree: {len(polynom_roots)} > {self._degree}")

    def _latex(self, polynom_first: ndarray[int | Fraction] | list[int | Fraction] | None, polynom_second: list[list[int|Fraction]] | None) -> str:
        """
        Метод преобразует списки/массивы в латех формат; только для полинома неканонического вида.
        Если требуется канонический вид полностью/частично, вызывается метод _latex_canon()

        :param polynom_first: "каноническая" часть итогового полинома, которая будет преобразована в _latex_canon()
        :type polynon_first: ndarray|list[int|Fraction]|None

        :param polynom_second: "неканоническая" часть полинома, которая будет преобразована в данном методе
        :type polynom_second: list[list[int|Fraction]]|None

        :param latex_polynom: преобразованный в латех формат полином
        :type latex_polynom: str

        :param exceptions: список, содержащий корни, которые были модифицированы в латех формат (нужен для того, чтобы
                           при выводе было (x-1)^2, а не (x-1)^2(x-1)^2)
        :type exceptions: list[list[int|Fraction]]

        :param numb: значение корня, которое подставляется в "скобку" полинома
        :type numb: str

        :param final_bracket: строка, которая представляет собой "одну" скобку полинома; в дальнейшем они собираются в
                              latex_polynom, т.е. принимают финальный вид
        :type final_bracket: str

        :return: сгенерированный полином в латех формате (если полином в каоническом виде, то подробности в _latex_canon)
        :rtype: str
        """
        latex_polynom: str = ""
        exceptions: list[list[int|Fraction]] = []
        if polynom_second is not None:
            for coef in polynom_second:
                if coef not in exceptions:
                    if coef != 0:
                        numb: str = self._latex_coef_modifier(coef[1])
                        final_bracket: str = (
                            "(%s%s)" % (self._variable, numb)
                            if self._multiplicity[coef[1] * -1] == 1
                            else "(%s%s)^%d"
                                 % (self._variable, numb, self._multiplicity[coef[1] * -1])
                        )
                        latex_polynom += final_bracket
                        exceptions.append(coef)
            if polynom_first is None:
                return f"{latex_polynom}"
            return f"{latex_polynom}{self._latex_canon(polynom_first)}"
        return f"{self._latex_canon(polynom_first)}"

    def _latex_canon(self, polynom: list) -> str:
        """

        :param polynom:
        :type polynom:

        :return:
        :rtype:
        """
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
        return f"({latex_string})"

    def _roots_setup(self) -> list[list[int | Fraction]]:
        """
        Метод преобразует изначальное введенное строковое значение корней
        в типы int или Fraction. На выходе получится список списков,
        каждое значение которого будет представлять из себя одну "скобку" полинома
        Например: [1, -1] -> (x-1); [[1,-1],[1,-2]] -> (x-1)(x-2)

        :param polynom: список списков, каждое значение которого будет представлять из себя одну "скобку" полинома
        :type polynom: list[list[int|Fraction]]

        :param multip_dict: вспомогательный словарь, который в дальшейшем станет self._multiplicity
        :type: dict[str | int, int]

        :return: список списков, каждое значение которого будет представлять из себя одну "скобку" полинома
        :rtype: list[list[int|Fraction]]
        """

        polynom: list[list[int | Fraction]] = []
        multip_dict: dict[str | int, int] = {}

        for key in self._multiplicity:
            self._roots.append(key)

        for root in self._roots:
            if "/" in root:
                root: Fraction = Fraction(root)
            else:
                root: int = int(root)
            polynom.append([1, -1 * root])

        self._roots.clear()
        for key in self._multiplicity:
            for count in range(self._multiplicity[key]):
                self._roots.append(key)

        for root in polynom:
            multip_dict[root[1] * -1] = self._multiplicity.get(str(root[1] * -1))
        self._multiplicity.clear()
        self._multiplicity = multip_dict.copy()

        return polynom

    @staticmethod
    def _latex_coef_modifier(numb: Fraction|int) -> str:
        """
        Метод для преобразования входящего значения в латех формат. Если знаменатель равен единице, число
        воспринимается как целое (int)

        :param numb: значение принимается с типом Fraction (может быть превращено в int, если знаменатель равен единице)
        :type numb: Fraction|int

        :return: преобразованное значение (\frac для дроби или +- *значение* для целых чисел)
        :rtype: str
        """
        if type(numb) == Fraction:
            if numb.denominator == 1:
                numb = int(numb.numerator)
            if numb.numerator < 0:
                return "-\\frac{%d}{%d}" % (numb.numerator * -1, numb.denominator)
            return "+\\frac{%d}{%d}" % (numb.numerator, numb.denominator)
        return "{:+}".format(numb)

    @staticmethod
    def _plus_minus_one(coef: str) -> str:
        """
        Вспомогательный метод, который преобразует "+1" и "-1" в "+" и "-" для корректного отображения в латехе

        :param coef: "+1" или "-1"
        :type coef: str

        :return: "+" или "-"
        :rtype: str
        """
        if coef == "+1":
            return "+"
        elif coef == "-1":
            return "-"
        return coef


a = PolynomGeneration(degree=7, multiplicity={'1': 1, '2': 1, '3/7': 5}, canon_view=False)
print(a.polynom_constructor())
