from flask import Blueprint, request
from services import GenerateTaskService
from generating_tasks_lib.utils.variants_generator import Task

generate_tasks_view = Blueprint('generate_tasks', __name__)


@generate_tasks_view.route('/', methods=['POST'])
def generate_tasks_handler():
    amount, variant = map_request(request.json)
    g = GenerateTaskService()
    return g.generate(amount, variant)


def map_request(request: dict) -> (int, list[Task]):
    amount = request.get('amount', 1)
    request_variant = request.get('variant', [])
    variant = []
    for request_task in request_variant:
        ttype = request_task.get('type', '')
        task = Task(ttype, {})
        variant.append(task)
    return amount, variant
