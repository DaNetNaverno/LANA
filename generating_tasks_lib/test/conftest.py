from random import randint

import pytest

from generating_tasks_lib.infinitesimal_functions import (
    InfinitesimalFunction, InfinitesimalFunctionsSettings)
from generating_tasks_lib.polynom_generation import (PolynomGeneration,
                                                     PolynomGenerationSettings)


@pytest.fixture(scope="session")
def infinitesimal_function() -> InfinitesimalFunction:
    inf_f = InfinitesimalFunction(InfinitesimalFunctionsSettings())
    inf_f.set_random_function()
    return inf_f


@pytest.fixture(scope="session")
def limit() -> str:
    return str(randint(-100, 100))


@pytest.fixture()
def polynom(limit: str) -> PolynomGeneration:
    return PolynomGeneration(
        5, [limit, "-2/3", "3/7"], False, {}, False, "x", PolynomGenerationSettings()
    )
