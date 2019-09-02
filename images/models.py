from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                                on_delete=models.CASCADE, related_name='images_created')
    #user.images_created.all()
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,
                                blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='image/%Y/%m/%d/')
    description = models.TextField(blank=True)  # description of the image
    created = models.DateField(auto_now_add=True,
                                db_index=True)
    # indexes improve query performance   
    # many-to-may field we can like multipe images and each image can be liked by multiple users
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                    related_name='images_liked',
                                    blank=True)
    # user.images_liked.all() or image.users_like.all()
    def get_absolute_url(self):
        return reverse("images:detail", args=[self.id, self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Image, self).save(*args, **kwargs)
