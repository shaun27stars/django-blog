from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.name()
