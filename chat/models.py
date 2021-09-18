from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Message(models.Model):
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
	receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
	timestamp = models.DateTimeField(default=timezone.now)
	content = models.CharField(max_length=1000)
