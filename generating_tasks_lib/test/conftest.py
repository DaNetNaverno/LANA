from random import randint

import pytest

from generating_tasks_lib.infinitesimal_functions import (
    InfinitesimalFunction,
    InfinitesimalFunctionsSettings,
)
from generating_tasks_lib.polynom_generation import (
    PolynomGeneration,
    PolynomGenerationSettings,
)


@pytest.fixture()
def infinitesimal_function() -> InfinitesimalFunction:
    inf_f = InfinitesimalFunction(InfinitesimalFunctionsSettings())
    return inf_f


@pytest.fixture()
def random_infinitesimal_function(
    infinitesimal_function: InfinitesimalFunction,
) -> InfinitesimalFunction:
    infinitesimal_function.set_random_function()
    return infinitesimal_function


@pytest.fixture()
def limit() -> str:
    return str(randint(-100, 100))


@pytest.fixture()
def polynom(limit: str) -> PolynomGeneration:
    return PolynomGeneration(
        degree=5, rational_coefs=False, multiplicity={limit: 1, "-2/3": 1, "3/7": 1}, canon_view=False, settings=PolynomGenerationSettings()
    )
