#title           :pyscript.py
#description     :Extend letucce for implemented BDD on Django.
#author          :juniorgerdet
#date            :04-06-2015
#version         :0.4
#usage           :python manager harvest
#notes           :
#python_version  :2.7.10  
#==============================================================================
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver

@receiver(pre_save, sender=User)
def my_handler(sender, **kwargs):
	print "save user"