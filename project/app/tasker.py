from datetime import datetime, timedelta
import hashlib, traceback

import requests
import numexpr as ne

from app import app, celery
from .models import db, Task


def function_evaluation(f, t):

    c = ne.evaluate(f)
    result = c.tolist()

    return result


def convert_timestamp(timestamp):

    return datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y')


def generating_points(f, today, start_day, dt):

    points = ((convert_timestamp(diff), function_evaluation(f, diff)) for diff in range(int(start_day),
                                                                                        int(today), dt*60*60))
    return points


def generation_images(f, td, sd, dt):

    points = generating_points(f, td, sd, dt)

    categories = []
    data = []

    for p1, p2 in points:
        categories.append(p1)
        data.append(p2)

    request_data =  {
                        "infile":{
                            "title":{
                                "text":"Steep Chart"
                                },
                                "xAxis":{
                                    "categories": categories,
                                },
                                "series":[
                                    {
                                        "data": data,
                                    }
                                ]
                            }
                        }

    r = requests.post('http://highcharts:8080', json=request_data)

    return r.content

@celery.task()
def task_processing(id):

    task_parameters = db.session.query(Task).filter(Task.id == id).first()

    f = task_parameters.function
    today = datetime.now()
    start_day = today - timedelta(days=task_parameters.interval)
    dt = task_parameters.step

    try:
        content = generation_images(f, today.timestamp(), start_day.timestamp(), dt)
    except Exception:
        err = traceback.format_exc()

        task_parameters.error = True
        task_parameters.error_msg = err
    else:

        hsh = hashlib.md5()
        hsh.update(content)
        hash_image = hsh.hexdigest()

        task_parameters.image_hash = hash_image
        task_parameters.image_data = content

    db.session.add(task_parameters)
    db.session.commit()


if __name__ == '__main__':

    pass
