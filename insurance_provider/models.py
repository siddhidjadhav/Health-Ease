from django.db import models

class Insurance(models.Model):
    insurance_name = models.CharField('Name', max_length=30)
    validity = models.IntegerField('Valid till')
    coverage = models.IntegerField('Coverage')
    # insurance_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.insurance_name
    