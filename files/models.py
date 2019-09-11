from django.db import models
from django.contrib.auth.models import User


class StagedSample(models.Model):
    def __str__(self):
        return str(self.sample_id)

    sample_id = models.IntegerField()
    nmol = models.FloatField()
    megareads = models.FloatField()
    priority = models.IntegerField()
    remark = models.CharField(max_length=100, default='')


class CombinationRestriction(models.Model):
    def __str__(self):
        return str(self.project_type1) + str(self.get_restriction_display()) + str(self.project_type2)
    project_type1 = models.IntegerField()
    project_type2 = models.IntegerField()
    restriction = models.BooleanField(choices=((True, ' is only allowed with '), (False, ' is not allowed with ')))
