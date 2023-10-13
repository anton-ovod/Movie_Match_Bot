import os
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("./templates/searching_dialogs/movie"))
