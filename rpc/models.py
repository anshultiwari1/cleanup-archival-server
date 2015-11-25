"""
StereoD.
Author  : Anshul Tiwari
Date    : Sep 30, 2015

Description : This holds all the model associated with shotinfo.
"""
'''
from django.contrib.contenttypes        import generic
from django.contrib.contenttypes.models import ContentType
from django.core        import serializers
from django.core.mail   import send_mail
from django.core.serializers.json import DjangoJSONEncoder
#from django.core.validators.json import MinValueValidator, MaxValueValidator
from django.db          import IntegrityError
from django.db          import models
from django.db.models   import Q
from django.db.models.signals import post_save
from django.dispatch    import receiver
from django.utils       import simplejson


class Shot(models.Model):
	title = models.CharField( max_length=500)
	owner = models.CharField( max_length=500)
	frameRange = models.CharField( max_length=500)
	renderTime = models.CharField( max_length=50)
	farmId = models.IntegerField( max_length=50)

'''