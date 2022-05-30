from django.db import models


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides
    self updating `created_on` and `updated_on` fields.
    """

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
