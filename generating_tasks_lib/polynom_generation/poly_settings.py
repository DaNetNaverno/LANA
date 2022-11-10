from pydantic import BaseSettings


class PolynomGenerationSettings(BaseSettings):
    int_lowest: int = -20
    int_highest: int = 20
    frac_lowest_num: int = -30
    frac_highest_num: int = 30
    frac_lowest_den: int = -10
    frac_highest_den: int = 10
