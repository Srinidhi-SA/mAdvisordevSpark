from __future__ import print_function
from __future__ import absolute_import
from builtins import str
from django.db.models.signals import post_save
from django.dispatch import receiver

from api.models import Dataset, Insight
from .utils import submit_job
from .models import Job
from .helper import JobserverDetails


@receiver(post_save, sender=Dataset)
def trigger_metadata_creation_job(sender, instance=None, created=False, **kwargs):
    print("Dataset got created, trigger a metadata job")
    if created:
        print("Dataset got created, trigger a metadata job")
        # TODO: Dataset got created, trigger a metadata job
        job = Job()
        job.name = "-".join(["Dataset", instance.slug])
        job.job_type = "metadata"
        job.object_id = str(instance.slug)
        job.config = "{}"
        job.save()

        job_url = submit_job(
            slug=job.slug,
            class_name='class_path_metadata'
        )

        job.url = job_url
        job.save()
        instance.job = job


@receiver(post_save, sender=Insight)
def trigger_insight_creation_job(sender, instance=None, created=False, **kwargs):
    if created:
        print("Signal got created, trigger a Insight job")
        # TODO: Signal got created, trigger a Insight job

        job = Job()
        job.name = "-".join(["Signal", instance.slug])
        job.job_type = "master"
        job.object_id = str(instance.slug)
        job.config = "{}"
        job.save()

        job_url = submit_job(
            slug=job.slug,
            class_name='class_path_metadata'
        )

        job.url = job_url
        job.save()
        instance.job = job

        # TODO: Write for filter also
