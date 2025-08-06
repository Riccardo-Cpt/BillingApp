from django.db import models

class ANAGRAPHIC_VIEW(models.Model):
  CD_SUPPLIER = models.CharField(max_length=255)
  CD_ADDRESS = models.CharField(max_length=255)
  CD_POD = models.CharField(max_length=255)
  FL_OFFER = models.CharField(max_length=255)
  FL_ANNUAL_EXP = models.FloatField(max_length=255)

   class Meta:
        db_table = "V_CURRENT_CUSTOMERS_COSTS"
        managed = False  # Instructs Django to ignore this during database migrations