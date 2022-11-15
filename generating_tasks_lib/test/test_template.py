from generating_tasks_lib.template.limit_template import EquivalenceLimits


class TestTemplate:
    def test_template_equival_latex(self, infinitesimal_function, polynom, limit):
        lim = EquivalenceLimits(
            f_x=polynom,
            g_x=polynom,
            inf_f=infinitesimal_function,
            inf_g=infinitesimal_function,
            limit=limit,
        )
        inf_f = infinitesimal_function
        inf_g = infinitesimal_function
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
