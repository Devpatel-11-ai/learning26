from django.db import models

# Create your models here.
class service(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=25)
    description = models.CharField()
    price = models.IntegerField(max_length=10)

    class Meta:
        db_table = 'Services'

    def __str__(self):
        return self.name 