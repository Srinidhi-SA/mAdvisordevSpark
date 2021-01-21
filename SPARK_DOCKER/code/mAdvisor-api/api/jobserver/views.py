
from sjsclient import client
from django.conf import settings
from api.helper import JobserverDetails


def submit_job(api_url, class_name):

    sjs = client.Client(
        JobserverDetails.get_jobserver_url()
    )

    app = sjs.apps.get(
        JobserverDetails.get_app()
    )

    ctx = sjs.contexts.get(
        JobserverDetails.get_context()
    )

    class_path = JobserverDetails.get_class_path(class_name)

    config = {
        'config_url': api_url
    }

    job = sjs.jobs.create(app, class_path, ctx=ctx, conf=config)

    # print
    JobserverDetails.print_job_details(job)
