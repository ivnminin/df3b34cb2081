from io import BytesIO

from flask import render_template, request, redirect, url_for, flash, send_file

from app import app
from .models import db, Task
from .forms import TaskForm
from .tasker import task_processing


@app.route('/')
def index():

    tasks = db.session.query(Task).order_by(db.desc(Task.updated_on)).all()

    return render_template('index.html', tasks=tasks)


@app.route('/add-task', methods=['GET', 'POST'])
def add_task():

    form =TaskForm()
    if request.method == 'POST' and form.validate_on_submit():

        t = Task(function=form.function.data, interval=form.interval.data, step=form.step.data)

        db.session.add_all([t])
        db.session.commit()

        job = task_processing.apply_async(args=[t.id], countdown=3)

        job.get()

        flash('Your changes have been saved.')
        return redirect(url_for('index'))

    return render_template('add_task.html', form=form)


@app.route('/download/<file_hash>')
def download(file_hash):

    image = db.session.query(Task).filter(Task.image_hash == file_hash).first_or_404()

    buf = BytesIO()
    buf.write(image.image_data)
    buf.seek(0)

    return send_file(buf, mimetype='image/png')


@app.errorhandler(404)
def http_404_handler(error):
    return "<p>HTTP 404 Error Encountered</p>", 404


@app.errorhandler(500)
def http_500_handler(error):
    return "<p>HTTP 500 Error Encountered</p>", 500
