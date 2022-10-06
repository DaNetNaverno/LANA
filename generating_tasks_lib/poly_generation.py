import random
from fractions import Fraction
from numpy import convolve


class PolynomGeneration:
    def __init__(self, degree: int, roots: list, rational_coefs: bool, multiplicity: int, canon_view: bool,
                 variable: str):
        self.degree = degree  # макс. степень полинома
        self.roots = roots  # введенные корни (вводить только с типом str!)
        self.rational_coefs = rational_coefs  # наличие рациональных коэффициентов
        self.multiplicity = multiplicity  # (x-a)^k отвечает за k
        self.canon_view = canon_view  # канонический вид
        self.variable = variable if variable == 'x' else '(' + variable + ')'  # переменная, по дефолту 'x'

    def full_random_generation(self):
        polynom = []
        for i in range(self.degree - len(self.roots) + 1):
            if not self.rational_coefs:
                polynom.append(random.randint(-20, 21))
            else:
                polynom.append(Fraction(random.randint(-20, 21), random.randint(1, 10)))
        return polynom

    def roots_generation(self):
        polynom = []
        for root in self.roots:
            if '/' in root:
                root = Fraction(root)
            else:
                root = int(root)
            polynom.append([1, -1 * root])
        return polynom

    def polynom_constructor(self):
        polynom_roots = self.roots_generation()
        polynom = self.full_random_generation()
        if self.canon_view:
            for i in polynom_roots:
                polynom = convolve(polynom, i)
            return self.latex(polynom, None)
        else:
            return self.latex(polynom, polynom_roots)

    def latex(self, polynom_first, polynom_second):
        latex_polynom = ''
        if polynom_second is not None:
            for i in polynom_second:
                if i != 0:
                    numb = self.latex_coef_modifier(self.fractions_checker(i[1]))
                    latex_polynom += '(%s%s)' % (self.variable, numb)
            return '\\[' + latex_polynom + self.latex_canon(polynom_first) + '\\]'
        else:
            return '\\[' + self.latex_canon(polynom_first) + '\\]'

    def latex_canon(self, polynom):
        latex_string = ''
        if self.canon_view:
            degree_mem = self.degree
        else:
            degree_mem = self.degree - len(self.roots)
        current_degree = degree_mem
        for i in polynom:
            coef = self.latex_coef_modifier(self.fractions_checker(i))
            if i != 0:
                if current_degree == degree_mem:
                    coef = self.plus_minus_one(coef)
                    if coef != '+':
                        if coef.startswith('+'):
                            latex_string += '%s%s^%d' % (coef[1::], self.variable, current_degree)
                        else:
                            latex_string += '%s%s^%d' % (coef, self.variable, current_degree)
                    else:
                        latex_string += '%s^%d' % (self.variable, current_degree)
                elif current_degree > 1:
                    coef = self.plus_minus_one(coef)
                    latex_string += '%s%s^%d' % (coef, self.variable, current_degree)
                elif current_degree == 1:
                    coef = self.plus_minus_one(coef)
                    latex_string += '%s%s' % (coef, self.variable)
                elif current_degree == 0:
                    latex_string += '%s' % coef
            current_degree -= 1
        if self.canon_view:
            return latex_string
        else:
            return '(' + latex_string + ')'

    @staticmethod
    def latex_coef_modifier(numb):
        if type(numb) == Fraction:
            if numb.numerator < 0:
                return '-\\frac{%d}{%d}' % (numb.numerator * -1, numb.denominator)
            else:
                return '+\\frac{%d}{%d}' % (numb.numerator, numb.denominator)
        else:
            return '{:+}'.format(numb)

    @staticmethod
    def fractions_checker(fract):
        if type(fract) == Fraction:
            if fract.denominator == 1:
                return fract.numerator
        return fract

    @staticmethod
    def plus_minus_one(coef):
        if coef == '+1':
            return '+'
        elif coef == '-1':
            return '-'
        return coef


a = PolynomGeneration(5, ['1', '-2/3', '3/7'], True, 1, True, 'x')
print(a.polynom_constructor())
