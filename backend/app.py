from sys import path


lib_path = next((x for x in path if "LANA/backend" in x),
                None).replace("LANA/backend", "LANA")
path.append(lib_path)

from flask import Flask
from handlers import generate_tasks_view


app = Flask(__name__)
app.register_blueprint(generate_tasks_view)
