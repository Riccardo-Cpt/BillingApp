from django.db import models

class Member(models.Model):
  CD_SUPPLIER = models.CharField(max_length=255)
  CD_ADDRESS = models.CharField(max_length=255)
  CD_POD = models.CharField(max_length=255)
  FL_OFFER = models.CharField(max_length=255)
  FL_ANNUAL_EXP = models.FloatField(max_length=255)