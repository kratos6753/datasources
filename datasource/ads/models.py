from django.db import models
from django.conf import settings
from uuid import uuid4
from django.utils.crypto import get_random_string

class BaseModel(models.Model):
  created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
  updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

  class Meta:
    abstract = True
  
  def save(self, *args, **kwargs):
    if 'update_fields' in kwargs and 'updated_at' not in kwargs['update_fields']:
      kwargs['update_fields'] = frozenset(list(kwargs['updated_fields']) + ['updated_at'])
    super(BaseModel, self).save(*args, **kwargs)

class ClientAPICredentials(BaseModel):
  client = models.OneToOneField(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='api_credentials'
  )
  api_key = models.CharField(max_length=32, unique=True, editable=False)
  api_secret = models.CharField(max_length=64, editable=False)
  is_active = models.BooleanField(default=True)

  def __str__(self):
    return f'API credentials for {self.client} - API Key : {self.api_key}'
  
  def save(self, *args, **kwargs):
    if not self.pk:
      self.api_key = uuid4().hex
      self.api_secret = get_random_string(64)
    super().save(*args, **kwargs)