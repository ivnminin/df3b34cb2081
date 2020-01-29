import click

from flask_script import Manager, Shell
from flask_migrate import MigrateCommand

from app import app, db
from app.models import Task

manager = Manager(app)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Task=Task)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@app.cli.command('start-project')
def start_project():
    """
    flask start project
    """
    db.create_all()


@app.cli.command('fake-data')
def fake_data():
    """
    flask fake-data
    """

    t = Task(function='function', interval=7, step=2)

    db.session.add_all([t])
    db.session.commit()


if __name__ == '__main__':
    manager.run()
