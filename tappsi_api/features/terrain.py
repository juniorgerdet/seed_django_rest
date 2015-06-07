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
from rest_framework.authtoken.models import Token
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
import datetime, re
from django.core.management.color import no_style
from django.db import connection
from django.utils.functional import curry

"""
Enable Log 
"""
logging.basicConfig(filename='logs/features.log',level=logging.INFO)

"""
Set PREFIX 
"""
STEP_PREFIX = r'(?:Given|And|Then|When) '

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
	try:
		world.response = world.rest.get(url,  format='json')
	except Exception, e:
		raise

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

@step('i get the responde code (\d+)')
def check_response(step, expected):
    code = world.response.status_code
    assert_equals(int(expected), code)

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
            user = User.objects.create(id=user_dict['id'], password=make_password(user_dict['password']), username=user_dict['username'], first_name=user_dict['first_name'], last_name=user_dict['last_name'])
            profile={"role_alt":user_dict['role_alt']}
            Profile.objects.create(user=user, **profile)
    else:
        expected_model=get_model('tappsi_api', model)
        data=hashes_data(step)
        for model_dict in data:
            logging.info('R: %s ', model_dict)
            a_model = expected_model(**model_dict)
            a_model.save()
    
@after.each_scenario
def sleep_scenario(step):
    if world.login:
    	print "Doing logout on tappsi_api..."
        world.rest.logout();
    time.sleep(1)

# logging.info('R: %s ', world.response)

def create_auth_client(Name, client_Id, client_Secret):
        user=User.objects.create_superuser(id=1000, username='root', password='Test10', email='root@email.com')
        return Application.objects.create(name=Name, client_id=client_Id, client_secret=client_Secret, user=user, 
                                   client_type=Application.CLIENT_CONFIDENTIAL,
                                   authorization_grant_type=Application.GRANT_PASSWORD)

"""
To Working with Django Models 
"""

def _models_generator():
    """
    Build a hash of model verbose names to models
    """
    for model in get_models():
        yield (unicode(model._meta.verbose_name), model)
        yield (unicode(model._meta.verbose_name_plural), model)


MODELS = dict(_models_generator())

_CREATE_MODEL = {}

def creates_models(model):
    """
    Register a model-specific creation function.
    """

    def decorated(func):
        """
        Decorator for the creation function.
        """
        _CREATE_MODEL[model] = func
        return func

    return decorated


_MODEL_EXISTS = {'tappsi_api.models.Ride': 'Ride', 'tappsi_api.models.Profile':'Profile'}


def checks_existence(model):
    """
    Register a model-specific existence check function.
    """

    def decorated(func):
        """
        Decorator for the existence function.
        """
        _MODEL_EXISTS[model] = func
        return func

    return decorated


def hash_data(hash_):
    """
    Convert strings from a Lettuce hash to appropriate types
    """
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
    """
    Convert strings from step hashes to appropriate types
    """
    return [hash_data(hash_) for hash_ in step.hashes]


def get_the_model(model):
    """
    Convert a model's verbose name to the model class. This allows us to
    use the models verbose name in steps.
    """

    name = model.lower()
    model = MODELS.get(model, None)

    assert model, "Could not locate model by name '%s'" % name

    return model


def reset_sequence(model):
    """
    Reset the ID sequence for a model.
    """
    sql = connection.ops.sequence_reset_sql(no_style(), [model])
    for cmd in sql:
        connection.cursor().execute(cmd)


def create_models(model, data):
    """
    Create models for each data hash.
    """
    if hasattr(data, 'hashes'):
        data = hashes_data(data)

    for hash_ in data:
        model.objects.create(**hash_)
    reset_sequence(model)


def _dump_model(model, attrs=None):
    """
    Dump the model fields for debugging.
    """

    for field in model._meta.fields:
        print '%s=%s,' % (field.name, str(getattr(model, field.name))),

    if attrs is not None:
        for attr in attrs:
            print '%s=%s,' % (attr, str(getattr(model, attr))),

    for field in model._meta.many_to_many:
        vals = getattr(model, field.name)
        print '%s=%s (%i),' % (
            field.name,
            ', '.join(map(str, vals.all())),
            vals.count()),

    print

def models_exist(model, data, queryset=None):
    """
    Check whether the models defined by @data exist in the @queryset.
    """

    if hasattr(data, 'hashes'):
        data = hashes_data(data)

    if not queryset:
        queryset = model.objects

    failed = 0
    try:
        for hash_ in data:
            fields = {}
            extra_attrs = {}
            for k, v in hash_.iteritems():
                if k.startswith('@'):
                    # this is an attribute
                    extra_attrs[k[1:]] = v
                else:
                    fields[k] = v

            filtered = queryset.filter(**fields)

            match = False
            if filtered.exists():
                for obj in filtered.all():
                    if all(getattr(obj, k) == v \
                            for k, v in extra_attrs.iteritems()):
                        match = True
                        break

            assert match, \
                "%s does not exist: %s\n%s" % (
                model.__name__, hash_, filtered.query)

    except AssertionError as exc:
        print exc
        failed += 1

    if failed:
        print "Rows in DB are:"
        for model in queryset.all():
            _dump_model(model, extra_attrs.keys())
        raise AssertionError("%i rows missing" % failed)

@step(r'I have(?: an?)? ([a-z][a-z0-9_ ]*) in the database:')
def create_models_generic(step, model):
    """
    And I have foos in the database:
        | name | bar  |
        | Baz  | Quux |

    The generic method can be overridden for a specific model by defining a
    function create_badgers(step), which creates the Badger model.
    """
    model = get_the_model(model)
    try:
        func = _CREATE_MODEL[model]
    except KeyError:
        func = curry(create_models, model)
    func(step)


@step(STEP_PREFIX + r'([A-Z][a-z0-9_ ]*) with ([a-z]+) "([^"]*)"' +
      r' has(?: an?)? ([A-Z][a-z0-9_ ]*) in the database:')
def create_models_for_relation(step, rel_model_name,
                               rel_key, rel_value, model):
    """
    And project with name "Ball Project" has goals in the database:
    | description                             |
    | To have fun playing with balls of twine |
    """

    lookup = {rel_key: rel_value}
    rel_model = get_the_model(rel_model_name).objects.get(**lookup)

    for hash_ in step.hashes:
        hash_['%s' % rel_model_name] = rel_model

    create_models_generic(step, model)


@step(STEP_PREFIX + r'(?:an? )?([A-Z][a-z0-9_ ]*) should be present ' +
      r'in the database')
def models_exist_generic(step, model):
    """
    *** Bug ***
    And objectives should be present in the database: 
    | description      |
    | Make a mess      |
    """
    if model=="User":
        for user_dict in step.hashes:
            user = User.objects.create(id=user_dict['id'], password=make_password(user_dict['password']), username=user_dict['username'], first_name=user_dict['first_name'], last_name=user_dict['last_name'])
            profile={"role_alt":user_dict['role_alt']}
            Profile.objects.create(user=user, **profile)
    else:
        model = get_the_model(model)
        try:
            func = _MODEL_EXISTS[model]
        except KeyError:
            func = curry(models_exist, model)
        func(step)


@step(r'There should be (\d+) ([a-z][a-z0-9_ ]*) in the database')
def model_count(step, count, model):
    """
    Then there should be 0 goals in the database
    """

    model = get_the_model(model)

    expected = int(count)
    found = model.objects.count()
    assert found == expected, "Expected %d %s, found %d." % \
        (expected, model._meta.verbose_name_plural, found)


def clean_db(scenario):
    """
    Clean the DB after each scenario

    Usage: after.each_scenario(clean_db)
    """

    call_command('flush', interactive=False)