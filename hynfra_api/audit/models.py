from django.db import models
from django.contrib.auth import get_user_model

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.
User = get_user_model()
class AuditLog(models.Model):
    action = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    details = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content_object = GenericForeignKey("content_type", "object_id")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,null=True,blank=True)
    object_id = models.PositiveIntegerField(
        null=True,
        blank=True
    )



    def __str__(self):
        return f"{self.action} by {self.user.username} at {self.timestamp}"