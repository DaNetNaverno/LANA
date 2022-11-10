from pydantic import BaseSettings


class PolynomGenerationSettings(BaseSettings):
    int_lowest: int = -1
    int_highest: int = 1
    frac_lowest_num: int = -10
    frac_highest_num: int = 10
    frac_lowest_den: int = -10
    frac_highest_den: int = 10
