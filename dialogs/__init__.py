from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("./templates/home_dialog"),
                  autoescape=True,
                  trim_blocks=True,
                  )


