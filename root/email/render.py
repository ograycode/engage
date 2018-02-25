import pybars


def render(source, data):
    compiler = pybars.Compiler()
    template = compiler.compile(source)
    return template(data)
