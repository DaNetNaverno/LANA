from generating_tasks_lib.utils.variants_generator import generate_variant, generate_variants, Task
from generating_tasks_lib.tasks import SumTaskOptions


class GenerateTaskService:
    def generate(self, amount: int, variant: list[Task]):
        variant = [
            Task('SUM', SumTaskOptions(0, 100, 5)),
            Task('SUM', SumTaskOptions(-50, 1000, 15)),
            Task('SUM', SumTaskOptions(10, 100, 2))
        ]
        return generate_variants(amount, variant)

# ,
