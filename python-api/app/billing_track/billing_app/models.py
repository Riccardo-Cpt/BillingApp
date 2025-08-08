from django.db import models

class ANAGRAPHIC_VIEW(models.Model):
  cd_supplier = models.CharField(max_length=255,  primary_key=True)
  cd_address = models.CharField(max_length=255)
  cd_pod = models.CharField(max_length=255)
  cd_offer = models.CharField(max_length=255)
  fl_annual_exp = models.FloatField()

  class Meta:
    db_table = "v_current_customers_costs"
    managed = False  # Instructs Django to ignore this during database migrations

  def __str__(self):
    return self.cd_supplier