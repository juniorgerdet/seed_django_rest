# -*- coding: utf-8 -*-
from lettuce import *
from rest_framework.test import APIRequestFactory, APIClient, force_authenticate
from django.core.management import call_command
from logging import getLogger
from django.test.client import Client
from nose.tools import assert_equals
import json, ast, logging, unicodedata
from tappsi_api.models import Rides
from django.contrib.auth.models import User
from oauth2_provider.models import Application


logging.basicConfig(filename='logs/features.log',level=logging.INFO)

@before.all
def set_browser():
    call_command('flush', interactive=False, verbosity=0)
    world.rest = APIClient()

@step(u'i have the payload')
def i_have_the_payload(step):
	world.payload=step.multiline


@step(r'i send a POST request on "([^"]*)"')
def i_send_a_get_request_on_url(step, url):
	try:
		payload = json.loads(world.payload.replace('\'', '"'))
		world.response = world.rest.post(url, payload,  format='json')
		# logging.info('R: %s ', world.response)
	except Exception, e:
		raise

@step(r'I send a GET request on "([^"]*)"')
def i_send_a_get_request_on_url(step, url):
	try:
		payload = json.loads(world.payload.replace('\'', '"'))
		world.response = world.rest.post(url, payload,  format='json')
		# logging.info('R: %s ', world.response)
	except Exception, e:
		raise

@step(r'I send a PUT request on "([^"]*)"')
def i_send_a_put_request_on_url(step, url):
	try:
		payload = json.loads(world.payload.replace('\'', '"'))
		world.response = world.rest.post(url, payload,  format='json')
		# logging.info('R: %s ', world.response)
	except Exception, e:
		raise

@step(r'I send a DELETE request on "([^"]*)"')
def i_send_a_delete_request_on_url(step, url):
	try:
		payload = json.loads(world.payload.replace('\'', '"'))
		world.response = world.rest.post(url, payload,  format='json')
		# logging.info('R: %s ', world.response)
	except Exception, e:
		raise

@step('i get the responde code (\d+)')
def check_response(step, expected):
    code = world.response.status_code
    assert_equals(int(expected), code)

@step('I get response data')
def check_response(step, expected):
    assert_equals(world.response.data, step.multiline)

@step('I authenticate as "(.*)"')
def i_authenticate(step, user):
	user = User.objects.get(username='lauren')
	world.rest.force_authenticate(user=user)

@step('i have user exists with username "(.*) and data')
def authen(step, model):
    model=models.get_model('tappsi_api', model)
    poll = Poll.objects.create(title=title)
    polls.save()

@step('a the following "(.*)"')
def i_have_the_following_model(step, model):
    model=models.get_model('tappsi_api', model)
    # poll = Poll.objects.create(title=title)
    # polls.save()

@step(r'I request "([^"]*)"')
def i_request_group(step, group):
	try:
		payload = json.loads(world.payload.replace('\'', '"'))
		world.response = world.rest.post(group, payload,  format='json')
		# logging.info('R: %s ', world.response)
	except Exception, e:
		raise