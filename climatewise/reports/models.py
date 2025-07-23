from django.db import models

# Create your models here.
class climate_report(models.Model):
    location = models.CharField(max_length=100)
    incident_type = models.CharField(max_length=50)
    ttime = models.DateTimeField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.incident_type} in {self.location} at {self.ttime}"


