from random import choice

from generating_tasks_lib.infinitesimal_functions.settings import \
    InfinitesimalFunctionsSettings
from generating_tasks_lib.infinitesimal_functions.utils import \
    get_infinitesimal_functions


class InfinitesimalFunction:
    def __init__(
        self,
        settings: InfinitesimalFunctionsSettings,
        infinitesimal_function: str | None = None,
    ):
        """
        :param settings: настройки для бесконечно малых функций
        :param infinitesimal_function: опциональный параметр, устанавливающий значение бесконечно малой функции
        """
        self._settings = settings
        self._infinitesimal_function: str | None = infinitesimal_function

    def set_function(self, infinitesimal_function: str) -> None:
        """
        Устанавливает значение бесконечно малой функции
        :param infinitesimal_function: значение бесконечно малой функции
        """
        self._infinitesimal_function = infinitesimal_function

    def set_random_function(
        self, infinitesimal_functions: list[str] | None = None
    ) -> None:
        """
        Устанавливает значение бесконечно малой функции, случайно выбраной из переданного списка
        :param infinitesimal_functions: список, бесконечно малых функций
        :return:
        """
        if not infinitesimal_functions:
            infinitesimal_functions = get_infinitesimal_functions(
                self._settings.infinitesimal_functions_path
            )
        self.set_function(choice(infinitesimal_functions))

    def set_param(self, param: int | str) -> None:
        """
        Устанавливает значение параметра a для бесконечно малой функции, если он есть
        :param param: значение параметра a
        :return:
        """
        self._infinitesimal_function = self._infinitesimal_function.replace(
            "<param>", f"{param}"
        )

    def compose(self, compose_function: str) -> None:
        """
        Создаёт композицию двух функций
        :param compose_function: функция, которая действует первой на x (f(g(x)), где g(x) переданная функция)
        """
        if not self._infinitesimal_function:
            raise ValueError("infinitesimal function is not specified")
        self._infinitesimal_function = self._infinitesimal_function.replace(
            "x", compose_function
        )

    def __str__(self) -> str:
        """
        Представляет функцию в формате tex
        :return: функция в формате tex
        """
        return (
            self._infinitesimal_function.replace("<(>", "{")
            .replace("<)>", "}")
            .replace("/#", "_{")
            .replace("#/", "}")
        )
