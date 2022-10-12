import json
from pathlib import Path


def get_infinitesimal_functions(path: Path) -> list[str] | None:
    """
    Получает список бесконечно малых функций из .json файла с путём path
    :param path: путь до файла
    :return:
    """
    with path.open("r") as file:
        return json.load(file).get("infinitesimal_functions")
