import random
from fractions import Fraction
from numpy import convolve, ndarray


class PolynomGeneration:
    def __init__(self, degree: int, roots: list, rational_coefs: bool, multiplicity: int, canon_view: bool,
                 variable: str):
        self.__degree = degree  # макс. степень полинома
        self.__roots = roots  # введенные корни (вводить только с типом str!)
        self.__rational_coefs = rational_coefs  # наличие рациональных коэффициентов
        self.__multiplicity = multiplicity  # (x-a)^k отвечает за k
        self.__canon_view = canon_view  # канонический вид
        self.__variable = variable if variable == 'x' else '(' + variable + ')'  # переменная, по дефолту 'x'

    def __full_random_generation(self) -> list:
        polynom: list = []
        for coef in range(self.__degree - len(self.__roots) + 1):
            if not self.__rational_coefs:
                polynom.append(random.randint(-20, 21))
            else:
                polynom.append(Fraction(random.randint(-20, 21), random.randint(1, 10)))
        return polynom

    def __roots_generation(self) -> list:
        polynom: list = []
        for root in self.__roots:
            if '/' in root:
                root: Fraction = Fraction(root)
            else:
                root: int = int(root)
            polynom.append([1, -1 * root])
        return polynom

    def polynom_constructor(self) -> str:
        polynom_roots: list = self.__roots_generation()
        if self.__degree > len(self.__roots):
            polynom = self.__full_random_generation()
            if self.__canon_view:
                for root in polynom_roots:
                    polynom = convolve(polynom, root)
                return self.__latex(polynom, None)
            else:
                return self.__latex(polynom, polynom_roots)
        elif self.__degree == len(self.__roots):
            if self.__canon_view:
                polynom = [1]
                for root in polynom_roots:
                    polynom = convolve(root, polynom)
                return self.__latex(polynom, None)
            else:
                return self.__latex(None, polynom_roots)
        else:
            raise Exception("len(roots) > degree")

    def __latex(self, polynom_first, polynom_second) -> str:
        latex_polynom: str = ''
        if polynom_second is not None:
            for coef in polynom_second:
                if coef != 0:
                    numb = self.__latex_coef_modifier(coef[1])
                    latex_polynom += '(%s%s)' % (self.__variable, numb)
            if polynom_first is None:
                return f'\\[{latex_polynom}\\]'
            if self.__multiplicity > 1:
                return f'\\[{latex_polynom}^{self.__multiplicity}{self.__latex_canon(polynom_first)}\\]'
            else:
                return f'\\[{latex_polynom}{self.__latex_canon(polynom_first)}\\]'
        else:
            return f'\\[{self.__latex_canon(polynom_first)}\\]'

    def __latex_canon(self, polynom: list) -> str:
        latex_string: str = ''
        if self.__canon_view:
            degree_mem: int = self.__degree
        else:
            degree_mem: int = self.__degree - len(self.__roots)
        current_degree: int = degree_mem
        for coef_orig in polynom:
            coef: str = self.__latex_coef_modifier(coef_orig)
            if coef_orig != 0:
                if current_degree == degree_mem and current_degree != 1:
                    coef = self.__plus_minus_one(coef)
                    if coef != '+':
                        if coef.startswith('+'):
                            latex_string += '%s%s^%d' % (coef[1::], self.__variable, current_degree)
                        else:
                            latex_string += '%s%s^%d' % (coef, self.__variable, current_degree)
                    else:
                        latex_string += '%s^%d' % (self.__variable, current_degree)
                elif current_degree > 1:
                    coef = self.__plus_minus_one(coef)
                    latex_string += '%s%s^%d' % (coef, self.__variable, current_degree)
                elif current_degree == 1:
                    coef = self.__plus_minus_one(coef)
                    if degree_mem == 1:
                        if coef.startswith('+'):
                            coef = coef[1::]
                    latex_string += '%s%s' % (coef, self.__variable)
                elif current_degree == 0:
                    latex_string += '%s' % coef
            current_degree -= 1
        if self.__canon_view:
            return latex_string
        else:
            return f'({latex_string})'

    @staticmethod
    def __latex_coef_modifier(numb) -> str:
        if type(numb) == Fraction:
            if numb.denominator == 1:
                numb = numb.numerator
        if type(numb) == Fraction:
            if numb.numerator < 0:
                return '-\\frac{%d}{%d}' % (numb.numerator * -1, numb.denominator)
            else:
                return '+\\frac{%d}{%d}' % (numb.numerator, numb.denominator)
        else:
            return '{:+}'.format(numb)

    @staticmethod
    def __plus_minus_one(coef: str) -> str:
        if coef == '+1':
            return '+'
        elif coef == '-1':
            return '-'
        return coef


#a = PolynomGeneration(3, ['3/1', '1/3'], False, 1, True, 'x')
#print(a.polynom_constructor())
