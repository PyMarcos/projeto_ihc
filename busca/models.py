from django.conf import settings
from django.db import models

# Create your models here.
from django_facebook.models import FacebookModel
from django.db import models
from django.dispatch.dispatcher import receiver
from django_facebook.models import FacebookModel
from django.db.models.signals import post_save
from django_facebook.utils import get_user_model, get_profile_model


class Busca(models.Model):
	busca = models.CharField(max_length = 100)
