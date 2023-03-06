import random
from fractions import Fraction

import numpy
from numpy import convolve, ndarray
from poly_settings import PolynomGenerationSettings


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
            roots: list[str],
            rational_coefs: bool = False,
            multiplicity: dict = dict({}),
            canon_view: bool = False,
            variable: str = 'x',
            settings: PolynomGenerationSettings = PolynomGenerationSettings(),
    ):
        self._degree = degree
        self._roots = roots
        self._rational_coefs = rational_coefs  #
        self._multiplicity = (
            multiplicity
        )
        self._canon_view = canon_view
        self._variable = (
            variable if variable == "x" else "(" + variable + ")"
        )
        self._settings = settings

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
        if len(self._roots) == 0:
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

    def _roots_generation(self) -> list[list[int | Fraction]]:
        """
        Метод преобразует изначальное введенное строковое значение корней
        в типы int или Fraction. На выходе получится список списков,
        каждое значение которого будет представлять из себя одну "скобку" полинома
        Например: [1, -1] -> (x-1); [[1,-1],[1,-2]] -> (x-1)(x-2)

        :param polynom: список списков, каждое значение которого будет представлять из себя одну "скобку" полинома
        :type polynom: list[list[int|Fraction]]

        :return: список списков, каждое значение которого будет представлять из себя одну "скобку" полинома
        :rtype: list[list[int|Fraction]]
        """
        polynom: list[list[int | Fraction]] = []
        for root in self._roots:
            if "/" in root:
                root: Fraction = Fraction(root)
            else:
                root: int = int(root)
            polynom.append([1, -1 * root])
        return polynom

    def polynom_constructor(self) -> str:
        """
        !!! Основной метод, который необходимо вызывать для генерации полинома !!!
        Главным образом объединяет работу большинства методов класса
        В дополнение проверяет, имеется ли непреднамеренное совпадение корней и преображает полином в канонический вид
        в случае необходимости (на уровне массива)

        :param polynom_roots: список списков, каждое значение которого будет представлять из себя одну "скобку" полинома
                              [подробности в _roots_generation()]
        :type polynom_roots: list[list[int|Fraction]]

        :param polynom: список сгенерированных коэффициентов полинома
                        [подробности в _full_random_generation()]
        :type polynom: list[int|Fraction]

        :param polynom_check: корни сгенерированного в _full_random_generation() полинома
        :type polynom_check: ndarray[numpy.complex128|numpy.float64]

        :param polynom_arr: массив, содержащий коэффициенты канонического полинома
        :type polynom_arr: ndarray[int|Fraction]

        :return: сгенерированный полином в латех формате (подробности в _latex())
        :rtype: str
        """
        polynom_roots: list[list[int | Fraction]] = self._roots_generation()
        self.multiplicity_setup(polynom_roots)
        polynom_arr: ndarray[int | Fraction] = numpy.array([1], dtype=numpy.int64)
        if self._degree > len(self._roots):
            while True:
                polynom: list[int | Fraction] = self._full_random_generation()
                polynom_check: ndarray[numpy.complex128|numpy.float64|numpy.int64] = numpy.roots(polynom)
                if not (set(polynom_check) & set(list(map(numpy.float64, self._roots)))):
                    break
            if self._canon_view:
                polynom_arr = convolve(polynom_arr, polynom)
                for root in polynom_roots:
                    polynom_arr = convolve(polynom_arr, root)
                return self._latex(polynom_arr, None)
            else:
                return self._latex(polynom, polynom_roots)
        elif self._degree == len(self._roots):
            if self._canon_view:
                polynom_arr = numpy.array([1], dtype=numpy.int64)
                for root in polynom_roots:
                    polynom_arr = convolve(root, polynom_arr)
                return self._latex(polynom_arr, None)
            else:
                return self._latex(None, polynom_roots)
        else:
            raise Exception("len(roots) > degree")

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
            else:
                return f"{latex_polynom}{self._latex_canon(polynom_first)}"
        else:
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
        else:
            return f"({latex_string})"

    def multiplicity_setup(self, polynom_roots: list) -> None:
        """

        :param polynom_roots:
        :return:
        """
        multip_dict: dict = {}
        for root in polynom_roots:
            multip_dict[root[1] * -1] = multip_dict.get(root[1] * -1, 0) + 1
        for value in multip_dict:
            if type(value) == Fraction:
                value_str: str = f"{value.numerator}/{value.denominator}"
            else:
                value_str: str = str(value)
            try:
                if self._multiplicity[value_str] > 1:
                    multip_dict[value] = (
                            multip_dict.get(value, 0) + self._multiplicity[value_str] - 1
                    )
            except KeyError:
                continue
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
            raise Exception("degree error( degree < len(roots) )")

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
        if type(numb) == Fraction:
            if numb.numerator < 0:
                return "-\\frac{%d}{%d}" % (numb.numerator * -1, numb.denominator)
            else:
                return "+\\frac{%d}{%d}" % (numb.numerator, numb.denominator)
        else:
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


sett = PolynomGenerationSettings()
a = PolynomGeneration(degree=6, roots=['1', '5', '2', '2'], canon_view=False)
# a = PolynomGeneration(degree=3, roots=['1', '2'], rational_coefs=False, multiplicity={}, canon_view=False, variable='x', settings=sett)
print(a.polynom_constructor())
