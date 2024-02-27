from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("./templates/searching_dialogs/"),
                  autoescape=True,
                  trim_blocks=True,
                  )
