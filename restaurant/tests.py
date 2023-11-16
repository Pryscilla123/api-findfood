import pytest
from decouple import config
from rest_framework.test import APIRequestFactory
from django.test import TestCase


# Create your tests here.


# @pytest.fixture
# def factory():
#     return APIRequestFactory()
#
#
# @pytest.fixture
# def user(factory):
#     request = factory.post('/api/token/',
#                            {'username': config('ADMINISTER_USER'), 'password': config('ADMINISTER_PASSWORD')},
#                            format='json')
#     return request
#
#
# def test_create_restaurant(user):
#     print(user)
#
#     assert True

def test_pytest_working():
    assert True == True
