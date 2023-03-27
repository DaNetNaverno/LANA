from generating_tasks_lib.infinitesimal_functions import InfinitesimalFunction
from generating_tasks_lib.polynom_generation import PolynomGeneration


class EquivalenceLimits:
    def __init__(
        self,
        f_x: PolynomGeneration,
        g_x: PolynomGeneration,
        inf_f: InfinitesimalFunction,
        inf_g: InfinitesimalFunction,
        limit: str,
    ):
        """
        :param f_x: первый полином f(x)
        :param g_x: второй полином g(x)
        :param inf_f: БМФ для первой функции f(x)
        :param inf_g: БМФ для первой функции g(x)
        :param limit: предел x0
        """
        self._f_x = f_x  # первый полином f(x)
        self._g_x = g_x  # второй полином g(x)
        self._inf_f = inf_f  # БМФ для первой функции f(x)
        self._inf_g = inf_g  # БМФ для первой функции g(x)
        self._limit = limit  #

    @property
    def equival_latex(self) -> str:
        """
        Оно работает!!! Наверное, генерирует задание с проверкой эквивалентностью 2-х функций
        :return:
        """
        self._inf_f.compose(self._f_x.polynom_constructor())
        self._inf_g.compose(self._g_x.polynom_constructor())
        return (
            (
                "\lim\limits_{x\\to "
                + self._limit
                + "} \\frac{"
                + str(self._inf_f)
                + "}{"
                + str(self._inf_g)
                + "}"
            )
            .replace("\[", "")
            .replace("\]", "")
        )
