from jinja2 import environment

def generate_custom_filter(app):

    def view_status(value):

        return value

    environment.DEFAULT_FILTERS['view_status'] = view_status