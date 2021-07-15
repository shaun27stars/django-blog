from django.db import models
from django.urls import reverse
from django.core.validators import MinLengthValidator

from .author import Author
from .tag import Tag


class Post(models.Model):
    title = models.CharField(max_length=50, unique=True)
    date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    excerpt = models.CharField(max_length=200)
    content = models.TextField(validators=[MinLengthValidator(30)])
    image = models.ImageField(upload_to='images')
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self) -> str:
        return f"{self.title} ({self.date})"

    def get_absolute_url(self):
        return reverse('post-detail', args=[self.slug])

    def sorted_comments(self):
        return self.comments.order_by('-id')

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     return super().save(*args, **kwargs)
