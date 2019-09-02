from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Action(models.Model):
    user = models.ForeignKey('auth.User',
                            related_name='actions',
                            on_delete=models.CASCADE,
                            db_index=True)  # user.actions.all()

    verb = models.CharField(max_length=255)
    # this will point to the model of the relationship.
    target_ct = models.ForeignKey(ContentType,
                                    null=True,
                                    blank=True,
                                    on_delete=models.CASCADE,
                                    related_name='target_obj')

    # thill will hold the primary key of the object
    target_id = models.PositiveIntegerField(null=True,
                                        blank=True,
                                        db_index=True)
    #genericForeignkey combines the id and model to obtain the object of the given model
    target = GenericForeignKey('target_ct', 'target_id')
    created = models.DateTimeField(auto_now_add=True,
                                    db_index=True)
    # both fields have null and blank as true because a target object is not
    # required while saving an action.

    class Meta:
        ordering = ('-created',)
