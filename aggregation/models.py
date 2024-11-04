from django.db import models
import uuid

# Create your models here.
class Charts(models.Model):
    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False)
    type = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    x_label = models.CharField(max_length=100, null=True, blank=True)
    variable = models.CharField(max_length=100, null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return self.name
