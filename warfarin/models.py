from django.db import models

# Create your models here.
class InputData(models.Model):
    create_date = models.DateTimeField()
    sex = models.FloatField()
    age = models.FloatField()
    bwt = models.FloatField()
    ht = models.FloatField()
    PTINR_1 = models.FloatField()
    PTINR_2 = models.FloatField()
    PTINR_3 = models.FloatField()
    PTINR_4 = models.FloatField()
    WFR_1 = models.FloatField()
    WFR_2 = models.FloatField()
    WFR_3 = models.FloatField()
