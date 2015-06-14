#title           :pyscript.py
#description     :Extend letucce for implemented BDD on Django.
#author          :juniorgerdet
#date            :04-06-2015
#version         :0.1
#usage           :python manager harvest
#notes           :
#python_version  :2.7.10  
#==============================================================================
# -*- coding: utf-8 -*-
from lettuce import *
from rest_framework.test import APIRequestFactory, APIClient, force_authenticate
from django.core.management import call_command
from logging import getLogger
from django.test.client import Client
from nose.tools import assert_equals
import json, ast, logging, unicodedata, time
from django.contrib.auth.models import User
from tappsi_api.models import Profile, Driver, Ride
from oauth2_provider.models import Application, AccessToken
from django.db.models.loading import get_models, get_model
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.core.management.color import no_style
import datetime, re

logging.getLogger('tappsi_api')
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',filename='logs/features.log',level=logging.INFO)

@before.all
def set_browser():
    world.rest = APIClient()

@before.each_scenario
def clean_scenario(step):
    world.login=False
    call_command('flush', interactive=False, verbosity=0)

@step(u'Register the app')
def register_the_app(step):
    for app_dict in step.hashes:
        world.app_id=create_auth_client(app_dict['name'], app_dict['client_id'], app_dict['client_secret'])

"""
Doing request django rest framework  
"""

@step(u'i have the payload')
def i_have_the_payload(step):
    world.payload = json.loads(step.multiline.replace('\'', '"'))

@step(r'i send a POST request on "([^"]*)"')
def i_send_a_get_request_on_url(step, url):
		world.response = world.rest.post(url, world.payload,  format='json')

@step(r'I send a GET request on "([^"]*)"')
def i_send_a_get_request_on_url(step, url):
    print url
    world.response = world.rest.get(url)
    logging.info('R: %s ', url)


@step(r'I send a PUT request on "([^"]*)"')
def i_send_a_put_request_on_url(step, url):
	try:
		world.response = world.rest.post(url, world.payload,  format='json')
	except Exception, e:
		raise

@step(r'I send a DELETE request on "([^"]*)"')
def i_send_a_delete_request_on_url(step, url):
	try:
		world.response = world.rest.post(url, world.payload,  format='json')
	except Exception, e:
		raise

@step('i get the response code (\d+)')
def check_response(step, expected):
    code = world.response.status_code
    assert_equals(int(expected), code)

@step('I get the response data with (\d+) items')
def count_data_response(step, expected):
    count = world.response.data["count"]
    assert_equals(int(expected), count)


@step('I get response data')
def check_response(step, expected):
    assert_equals(world.response.data, step.multiline)


@step('I authenticate as user "(.*)"')
def i_authenticate(step, user):
    user = User.objects.get(username=user)
    access_token = AccessToken.objects.create(
        user=user, token='WpcQH4L8Lf99cuQ2kWwITY8DD9xxM3',
        application=world.app_id, scope='read write',
        expires=timezone.now() + datetime.timedelta(days=1)
    )
    try:
        world.login=world.rest.credentials(HTTP_AUTHORIZATION='Bearer ' + "WpcQH4L8Lf99cuQ2kWwITY8DD9xxM3")
        world.login=True
    except Exception, e:
        raise

@step('I have user exists with username "(.*) and data')
def authen(step, model):
    model=models.get_model('tappsi_api', model)
    poll = Poll.objects.create(title=title)
    polls.save()

@step(r'The following data on ([A-Z][a-z0-9_ ]*)')
def the_following_data_on_model(step, model):
    if model=="User":
    	for user_dict in step.hashes:
            logging.info('R: %s ', user_dict)
            user = User.objects.create(id=user_dict['id'], password=make_password(user_dict['password']), username=user_dict['username'], email=user_dict['email'], first_name=user_dict['first_name'], last_name=user_dict['last_name'])
            profile={"role_alt":user_dict['role_alt']}
            Profile.objects.create(user=user, **profile)
        if profile['role_alt']!="client":
            Driver.objects.create(user=user)
    else:
        expected_model=get_model('tappsi_api', model)
        data=hashes_data(step)
        for model_dict in data:
            a_model = expected_model(**model_dict)
            a_model.save()
                
@after.each_scenario
def sleep_scenario(step):
    if world.login:
    	print "Doing logout on tappsi_api..."
        # world.rest.logout();
    time.sleep(1)

# logging.info('R: %s ', world.response)

def create_auth_client(Name, client_Id, client_Secret):
        user=User.objects.create_superuser(id=1000, username='root', password='Test10', email='root@email.com')
        return Application.objects.create(name=Name, client_id=client_Id, client_secret=client_Secret, user=user, 
                                   client_type=Application.CLIENT_CONFIDENTIAL,
                                   authorization_grant_type=Application.GRANT_PASSWORD)

def hash_data(hash_):
    res = {}
    for key, value in hash_.items():
        if type(value) in (str, unicode):
            if value == "true":
                value = 1
            elif value == "false":
                value = 0
            elif value == "null":
                value = None
            elif value.isdigit() and not re.match("^0[0-9]+", value):
                value = int(value)
            elif re.match(r'^\d{4}-\d{2}-\d{2}$', value):
                value = datetime.strptime(value, "%Y-%m-%d")
        res[key] = value
    return res

def hashes_data(step):
    return [hash_data(hash_) for hash_ in step.hashes]
