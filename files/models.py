from django.db import models
from django.contrib.auth.models import User


class StagedSamples(models.Model):
    def __str__(self):
        return str(self.sample_id)

    sample_id = models.IntegerField()
    nmol = models.FloatField()
    megareads = models.FloatField()
