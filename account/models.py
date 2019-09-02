from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


# to extend the user model
# add an additional field to the a model called profile(or whatever the heck you wanna name it)
# and include a one-to-one relationship with the user model.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return "Profile for user: {}".format(self.user.username)

# we are creating an intermediary model for the many-to-may field. because
# 1. We are creating a relationship between the user model we want to avoid altering it.
# 2. We want to store some additional info, eg time relationship was formed.
class Contact(models.Model):
    # the user initiating the realtionship
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE, related_name='rel_from_set')
    # the user being followed.
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE, related_name='rel_to_set')
    created = models.DateTimeField(auto_now_add=True,
                                    db_index=True)
    
    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return "{} follows {}".format(self.user_from, self.user_to)


User.add_to_class('following',
                    models.ManyToManyField(
                        'self',
                        through=Contact,
                        related_name='followers',
                        symmetrical=False,
                    ))