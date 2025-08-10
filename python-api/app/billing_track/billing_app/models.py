from django.db import models

class ANAGRAPHIC_VIEW(models.Model):
  pk_bill_period = models.CharField(max_length=255, primary_key=True)
  pk_supplier = models.CharField(max_length=255)
  cd_address = models.CharField(max_length=255)
  pk_pod = models.CharField(max_length=255)
  cd_offer = models.CharField(max_length=255)

  class Meta:
    db_table = "v_current_customers_costs"
    managed = False  # Instructs Django to ignore this during database migrations
    # Define a composite unique constraint
    constraints = [
            models.UniqueConstraint(fields=['pk_bill_period', 'pk_supplier', 'pk_pod'], name='pk_current_customer_costs')
        ]

  def __str__(self):
    return f"{self.pk_bill_period} {self.pk_supplier} {self.pk_pod}"