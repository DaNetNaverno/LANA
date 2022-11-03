import random
import numpy as np
from fractions import Fraction
from numpy import convolve
import sympy
import matplotlib.pyplot as plt

class PolynomGeneration:
    def __init__(self, degree: int, roots: list, rational_coefs: bool, multiplicity: int, canon_view: bool,
                 variable: str):
        self.degree = degree  # макс. степень полинома
        self.roots = roots  # введенные корни (вводить только с типом str!)
        self.rational_coefs = rational_coefs  # наличие рациональных коэффициентов
        self.multiplicity = multiplicity  # (x-a)^k отвечает за k
        self.canon_view = canon_view  # канонический вид
        self.variable = variable if variable == 'x' else variable  # переменная, по дефолту 'x'

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


class Integral:
    def __init__ (self):
        self.degree: int = random.randint(2,5) #степень многочлена в знаменателе
        self.variable: str = 'x' #переменная 
        self.multiplicity = 1

    def integral_constructor(self): #функция генерации интеграла
        self.roots: list[str] =  self.random_roots_generation() #генерация случайных корней многочлена
        self.random_border_generation()
        b = PolynomGeneration(self.degree, self.roots, True, self.multiplicity, False, self.variable) #генерация многочлена со случайными корнями
        self.polynom: str = b.polynom_constructor()
        self.polynom = self.polynom[2:len(self.polynom)-2]

        if self.polynom[self.polynom.find('x^0')-1] == '(':
            self.polynom = self.polynom[0:len(self.polynom)-6] + ')'
        elif self.polynom[self.polynom.find('x^0')-1] == '-':
            self.polynom = '-' + self.polynom[0:len(self.polynom)-6]
        else:
            self.polynom = self.polynom[0:len(self.polynom)-4]+')'

        self.latex()
            
        return self.integral

    def random_roots_generation(self): #функция генерации случайных корней
        roots: list[str] = []
        for i in range(self.degree-self.multiplicity+1):
            # if (random.randint(0, 1)):
            #     roots.append(str(random.randint(-10,10)) + '/' + str(random.randint(1,10)))
            # else:
            roots.append(str(random.randint(-10, 10)))
        return roots

    # Пофиксить генерацию

    def random_border_generation(self): #генерация границ интегрирования
        if (random.randint(0, 1)):
            self.up_border = '+\\' + str(np.inf) + 'ty'
        else:
            if (random.randint(0, 1)):
                self.up_border = random.randint(-10,10)
            else:
                self.up_border = Fraction(random.randint(-10,10), random.randint(1,10))
        if (random.randint(0, 1)):
            self.low_border = '-\\' + str(np.inf) + 'ty'
        else:
            if (random.randint(0, 1)):
                self.low_border = random.randint(-10, 10)
            else:
                self.low_border = Fraction(random.randint(-10,10), random.randint(1,10))

        if (type(self.low_border) != str and type(self.up_border) != str):
            if self.low_border > self.up_border:
                self.low_border, self.up_border = self.up_border, self.low_border
                if (not self.check_roots()):
                    self.low_border = min(self.roots, key=lambda x: Fraction(x))

    def check_roots(self):
        for root in self.roots:
            if (Fraction(root) > self.low_border or Fraction(root) < self.up_border):
                return True
        return False

    def latex(self): #функция преобразования в LaTeX формат
        self.integral:str = ('\\int_{%s}^{%s}' % (str(self.latex_coef_modifier(self.low_border)), str(self.latex_coef_modifier(self.up_border)))
                        + ' \\frac{%s}' % ('\\mathrm{d}{%s}' % (self.variable))
                        + '{%s}' % (self.polynom))

    @staticmethod
    def latex_coef_modifier(numb):
        if type(numb) == Fraction:
            if numb.numerator < 0:
                if (numb.denominator != 1):
                    return '-\\frac{%d}{%d}' % (numb.numerator * -1, numb.denominator)
                else:
                    return '-\\{%d}' % (numb.numerator * -1)

            else:
                if (numb.denominator != 1):
                    return '\\frac{%d}{%d}' % (numb.numerator, numb.denominator)
                else:
                    return '\\{%d}' % (numb.numerator)
        elif type(numb) != str:
            return numb
        else:
            return numb

    def solve_integral(self):
        table = np.empty((0, self.degree))
        polynoms: list[str] = []
        tmp_roots = ['10', '1/2']
        for i in range(self.degree):
            tmp = PolynomGeneration(self.degree-1 ,self.roots[0:i]+self.roots[i+1:], False, 1, True, 'x')
            polynoms.append(tmp.polynom_constructor())

        # Выделение коэффицентов
        for polynom in polynoms:
            # print(polynom)
            coefs: list[str] = []
            polynom = polynom[2:len(polynom)-2]
            print(polynom)

            # polynom = '-11x^1'
            # self.degree = 1
            if (polynom[:polynom.find('x^'+str(self.degree-1))] == '' or polynom[:polynom.find('x^'+str(self.degree-1))] == '-'):
                coefs.append(polynom[:polynom.find('x^'+str(self.degree-1))] + '1')
            else:
                if (self.degree == 1):
                    coefs.append(polynom[:polynom.find('x^'+str(self.degree-1))-2])
                else:
                    coefs.append(polynom[:polynom.find('x^'+str(self.degree-1))])

            
            # print(polynom)
            for i in range(2,self.degree-1):
                if (polynom.find('x^'+str(self.degree-i)) != -1):
                    tmp = polynom[:polynom.find('x^'+str(self.degree-i))]
                    if (tmp[tmp.rfind('x')+3:] == '-' or tmp[tmp.rfind('x')+3:] == '+'):
                        coefs.append(tmp[tmp.rfind('x')+3:] + '1')
                    else:
                        coefs.append(tmp[tmp.rfind('x')+3:])
                else:
                    coefs.append('0')                    
            if (self.degree-1 != 1):
                if (polynom.rfind('x') != polynom.rfind('x^')):
                    tmp = polynom[:polynom.rfind('x')]
                    if (tmp[tmp.rfind('x')+3:] == '-' or tmp[tmp.rfind('x')+3:] == '+'):
                        coefs.append(tmp[tmp.rfind('x')+3:] + '1')
                    else:
                        coefs.append(tmp[tmp.rfind('x')+3:])
                else:
                    coefs.append('0')
            if (polynom.rfind('x') != len(polynom)-1):
                if (polynom.find('x^1') == -1):
                    if (polynom.rfind('x') != polynom.rfind('x^')):
                        coefs.append(polynom[polynom.rfind('x')+1:])
                    else:
                        coefs.append(polynom[polynom.rfind('x^')+3:])
                else:
                    if (polynom[polynom.find('x^1')+3:] != ''):
                        coefs.append(polynom[polynom.find('x^1')+3:])
            else:
                coefs.append('0')

            tmp_list: list[float] = []
            for coef in coefs:
                if (coef.find('frac') != -1):
                    sign = coef[0]
                    numer = coef[coef.find('{'):coef.rfind('{')]
                    numer = numer[1:len(numer)-1]
                    denomin = coef[coef.rfind('{'):]
                    denomin = denomin[1:len(denomin)-1]
                    tmp_list.append(float(Fraction(sign + numer + '/' + denomin)))
                else:
                    if (coef[0] == '+'):
                        tmp_list.append(float(coef[1:]))
                    else:
                        tmp_list.append(float(coef))
            table = np.append(table, np.array([tmp_list]), axis=0)
        tmp_free_coefs: list[float] = []


        for i in range(self.degree-1):
            tmp_free_coefs.append(float(0))
        tmp_free_coefs.append(float(1))
        free_coefs = np.array(tmp_free_coefs)
        table = table.transpose()
        print(table)
        # print(free_coefs)

        answers = np.linalg.solve(table, free_coefs)
        for answer in answers:
            print(Fraction(answer)) 
        print(self.low_border, self.up_border)
        result = 0

        # Подсчет ответа
        for root, answer in zip(self.roots, answers):
            if (self.low_border == '-\\infty' and self.up_border == '+\\infty'):
                print(1)
            elif (self.low_border == '-\\infty'):
                print(2)
            elif (self.up_border == '+\\infty'):
                print(3)
            else:
                print(4)


class Series:
    def __init__ (self):
        self.degree = random.randint(2, 5)
        self.variable: str = 'n'
        self.step: int = random.randint(2,6)

    def series_constructor(self): #функция генерации интеграла
        self.roots: list[str] =  self.random_roots_generation() #генерация случайных корней многочлена
        b = PolynomGeneration(self.degree, self.roots, True, 1, False, self.variable) #генерация многочлена со случайными корнями
        self.polynom: str = b.polynom_constructor() 
        self.polynom = self.polynom[2:len(self.polynom)-2]

        if self.polynom[self.polynom.find('n^0')-1] == '(':
            self.polynom = self.polynom[0:len(self.polynom)-6] + ')'
        elif self.polynom[self.polynom.find('n^0')-1] == '-':
            self.polynom = '-' + self.polynom[0:len(self.polynom)-6]
        else:
            self.polynom = self.polynom[0:len(self.polynom)-4]+')'


        self.latex()
        return self.series

    def random_roots_generation(self): #функция генерации случайных корней
        roots: list[str] = []
        if (random.randint(0, 1)):
            roots.append(str(random.randint(-100,100)) + '/' + str(random.randint(1,100)))
        else:
            roots.append(str(random.randint(-100, 100)))
        for i in range(1,self.degree):
            roots.append(str(Fraction(roots[i-1])+self.step))
        return roots

    def latex(self): #функция преобразования в LaTeX формат
        self.series:str = ('\\Sigma_{%s}^{%s}' % (str(1), '+\\infty')
                        + ' \\frac{%s}' % ('{%s}' % ('1'))
                        + '{%s}' % (self.polynom))


b = Integral()
ser = Series()
# c = PolynomGeneration(3, ['13/15', '14', '15'], True, 1, True, 'x')
# print(c.polynom_constructor())
expr = b.integral_constructor()
b.solve_integral()
# expr = ser.series_constructor()
print(expr)




M5 = np.array([[float(Fraction(13,16)), -6., 1.], [0., -3., 1], [-3, 0, 1]]) 
v5 = np.array([1., 2., -1.]) 
print(np.linalg.solve(M5, v5))


# plt.text(0, 0.6, r"$%s$" % expr, fontsize=50)

# fig = plt.gca()
# fig.axes.get_xaxis().set_visible(False)
# fig.axes.get_yaxis().set_visible(False)
# plt.draw()
# plt.show()


