import pytest

from generating_tasks_lib.infinitesimal_functions import InfinitesimalFunction
from generating_tasks_lib.template.limit_template import EquivalenceLimits


class TestTemplate:
    def test_template_equival_latex(
        self, random_infinitesimal_function: InfinitesimalFunction, polynom, limit
    ):
        lim = EquivalenceLimits(
            f_x=polynom,
            g_x=polynom,
            inf_f=random_infinitesimal_function,
            inf_g=random_infinitesimal_function,
            limit=limit,
        )
        inf_f = random_infinitesimal_function
        inf_g = random_infinitesimal_function
        inf_f.compose(polynom.polynom_constructor())
        inf_g.compose(polynom.polynom_constructor())
        assert lim.equival_latex == (
            "\lim\limits_{x\\to "
            + limit
            + "} \\frac{"
            + str(inf_f)
            + "}{"
            + str(inf_g)
            + "}"
        ).replace("\]", "").replace("\[", "")

    @pytest.mark.parametrize(
        "function,latex_form",
        [("\\sin<(>x<)>", "\\sin{x}"), ("<param>^<(>x<)>-1", "71^{x}-1")],
    )
    def test_template_infinitesimal_functions(
        self,
        infinitesimal_function: InfinitesimalFunction,
        function: str,
        latex_form: str,
    ):
        infinitesimal_function.set_function(function)
        infinitesimal_function.set_param(71)
        assert str(infinitesimal_function) == latex_form
