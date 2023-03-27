from enum import Enum

from generating_tasks_lib.data.latex_variant_template import latex_variant_template
from generating_tasks_lib.tasks import generate_sum_task


class Task:
    def __init__(self, ttype: str, options):
        self.type = ttype
        self.options = options


class TaskType(Enum):
    SUM = "SUM"


task_generators = {TaskType.SUM: generate_sum_task}


def generate_variant(number: int, variant: list[Task]) -> str:
    content = ""
    for task in variant:
        generator = task_generators[TaskType[task.type]]
        latex, res = generator(task.options)
        content += f"\item {latex}\n"
    return latex_variant_template.format(variant=number, content=content)


def generate_variants(amount: int, variant: list[Task]) -> str:
    content = ""
    for variant_number in range(amount):
        content += generate_variant(variant_number + 1, variant)
    return content
