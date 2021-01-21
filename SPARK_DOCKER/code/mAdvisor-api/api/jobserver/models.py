from django.db import models


class Job(models.Model):

    job_type = models.CharField(max_length=300, null=False)
    object_id = models.CharField(max_length=300, null=False)
    slug = models.SlugField(null=True)
    config = models.TextField(default="{}")
    results = models.TextField(default="{}")

    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)
    deleted = models.BooleanField(default=False)
