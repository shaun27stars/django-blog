from django.db import models


class Tag(models.Model):
    caption = models.CharField(max_length=30)

    def __str__(self):
        return self.caption
