from pathlib import Path

from pydantic import BaseSettings


class InfinitesimalFunctionsSettings(BaseSettings):
    infinitesimal_functions_path: Path = Path(
        "/LANA/generating_tasks_lib/data/infinitesimal_functions.json"
    )
