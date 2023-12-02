import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from utils.tools import Days
from datetime import datetime

# Create your tests here.


@pytest.fixture
def user():
    user = User.objects.create_superuser(username='admin', password='password', email='admin@example.com')
    return user


@pytest.fixture
def client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def restaurant_info():
    def make(name, type):
        return {
            "name": name,
            "type": type,
            "img": "https://res.cloudinary.com/doy0n9z9i/image/upload/v1699051941/k8vkkcfh4wabrk6fison.jpg"
        }

    return make


@pytest.fixture
def address_info():
    def make(line1, line2, restaurant_id):
        return {
            "line1": line1,
            "line2": line2,
            "number": 1,
            "postal_code": "12345-678",
            "restaurant_id": restaurant_id
        }

    return make


@pytest.fixture
def schedule_info():
    def make(day, restaurant_id):
        return [
            {
                "interval_id": {
                    "day": day,
                    "open": "12:00:00",
                    "close": "16:00:00"
                },
                "restaurant_id": restaurant_id
            }
        ]

    return make


@pytest.fixture
def contact_info():
    def make(restaurant_id):
        return [
            {
                "type": "insta",
                "information": "@bkinfos",
                "restaurant_id": restaurant_id,
            }
        ]
    return make


@pytest.fixture
def restaurant_data(restaurant_info, address_info, schedule_info, contact_info):
    def make(restaurant_id, address_id, schedule_id, interval_id, contact_id, is_open):
        restaurant_data = restaurant_info('bk', 'fastfood')
        address_data = address_info('rua da lagoa', 'bairro caixoeira', restaurant_id)
        address_data = {'id': address_id, **address_data}
        del address_data['restaurant_id']
        schedule_data = schedule_info('Quarta', restaurant_id)
        schedule_data[0] = {'id': schedule_id, **schedule_data[0]}
        del schedule_data[0]['restaurant_id']
        schedule_data[0]["interval_id"] = {'id': interval_id, **schedule_data[0]["interval_id"]}
        contact_data = contact_info(restaurant_id)
        contact_data[0] = {'id': contact_id, **contact_data[0]}
        del contact_data[0]['restaurant_id']
        return [
            {
                "id": restaurant_id,
                "name": restaurant_data["name"],
                "type": restaurant_data["type"],
                "restaurant_address": address_data,
                "opening_days": schedule_data,
                "socials": contact_data,
                "is_open": is_open,
                "img": 'image/upload/' + restaurant_data["img"],
            }
        ]
    return make


@pytest.fixture
def contact(client, contact_info):
    def make_contact(restaurant_id):
        response = client.post('/restaurant/contact/', contact_info(restaurant_id), format="json")
        return response
    return make_contact


@pytest.fixture
def restaurant(client, restaurant_info):
    def make_restaurant(name, type):
        response = client.post('/restaurant/management/', restaurant_info(name, type))
        return response

    return make_restaurant


@pytest.fixture
def address(client, address_info):
    def make_address(line1, line2, restaurant_id):
        response = client.post('/restaurant/address/', address_info(line1, line2, restaurant_id))
        return response

    return make_address


@pytest.fixture
def schedule(client, schedule_info):
    def make_schedule(day, restaurant_id):
        response = client.post('/restaurant/schedule/', schedule_info(day, restaurant_id), format='json')
        return response

    return make_schedule


@pytest.mark.django_db
def test_restaurant_post_request(restaurant):
    response = restaurant('bk', 'fastfood')
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_restaurant_put_request(restaurant, client, restaurant_info):
    restaurant = restaurant('bk', 'fastfood')
    restaurant_id = restaurant.data.get('id')
    response = client.put(f'/restaurant/management/{restaurant_id}/', restaurant_info('bk shakes', 'fastfood'))
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_restaurant_patch_request(restaurant, client):
    restaurant = restaurant('bk', 'fasfood')
    restaurant_id = restaurant.data.get('id')
    response = client.patch(f'/restaurant/management/{restaurant_id}/', {'name': 'bk shakes'})
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_restaurant_delete_request(restaurant, client):
    restaurant = restaurant('bk', 'fastfood')
    restaurant_id = restaurant.data.get('id')
    response = client.delete(f'/restaurant/management/{restaurant_id}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_restaurant_get_request(client, restaurant_data, restaurant, address, schedule, contact):
    restaurant = restaurant('bk', 'fastfood')
    restaurant_id = restaurant.data.get("id")
    address = address('rua da lagoa', 'bairro caixoeira', restaurant_id)
    address_id = address.data.get("id")
    schedule = schedule("Quarta", restaurant_id)
    schedule_id = dict(schedule.data[0]).get("id")
    interval_data = dict(dict(schedule.data[0])["interval_id"])
    interval_id = interval_data.get("id")
    contact = contact(restaurant_id)
    contact_id = dict(contact.data[0]).get("id")

    todays_day = Days[datetime.now().strftime('%A').upper()].value
    todays_time = datetime.now().time()
    open_day = interval_data.get("day")

    open = datetime.strptime(interval_data.get("open"), "%H:%M:%S").time()
    close = datetime.strptime(interval_data.get("close"), "%H:%M:%S").time()

    if open <= todays_time <= close and todays_day == open_day:
        is_open = True
    else:
        is_open = False

    restaurant_expected = restaurant_data(restaurant_id, address_id, schedule_id, interval_id, contact_id, is_open)

    response = client.get('/restaurant/management/')
    response_data = dict(response.data[0])
    response_data['restaurant_address'] = dict(response_data['restaurant_address'])
    response_data['opening_days'][0] = dict(response_data['opening_days'][0])
    response_data['opening_days'][0]['interval_id'] = dict(response_data['opening_days'][0]['interval_id'])
    response_data['socials'][0] = dict(response_data['socials'][0])

    assert response_data == restaurant_expected[0]


@pytest.mark.django_db
def test_restaurant_filter_is_open(client, restaurant, address, schedule, contact):
    restaurant = restaurant('bk', 'fastfood')
    restaurant_id = restaurant.data.get("id")
    _ = address('rua da lagoa', 'bairro caixoeira', restaurant_id)
    schedule = schedule("Quarta", restaurant_id)
    _ = contact(restaurant_id)

    interval_data = dict(dict(schedule.data[0])["interval_id"])

    todays_day = Days[datetime.now().strftime('%A').upper()].value
    todays_time = datetime.now().time()
    open_day = interval_data.get("day")

    open = datetime.strptime(interval_data.get("open"), "%H:%M:%S").time()
    close = datetime.strptime(interval_data.get("close"), "%H:%M:%S").time()

    if open <= todays_time <= close and todays_day == open_day:
        is_open = 'true'
    else:
        is_open = 'false'

    response = client.get(f'/restaurant/management/?is_open={is_open}')

    assert response.status_code == status.HTTP_200_OK and len(response.data) > 0


@pytest.mark.django_db
def test_address_post_request(restaurant, address):
    restaurant = restaurant('bk', 'fastfood')
    response = address('rua do restaurante', 'bairro do restaurante', restaurant.data.get('id'))
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_address_put_request(restaurant, address, address_info, client):
    restaurant = restaurant('bk', 'fastfood')
    address = address('rua do restaurante', 'bairro do restaurante', restaurant.data.get('id'))
    response = client.put(f'/restaurant/address/{address.data.get("id")}/',
                          address_info('rua das flores', 'bairro jardim', restaurant.data.get('id')))
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_address_patch_request(restaurant, address, client):
    restaurant = restaurant('bk', 'fastfood')
    address = address('rua do restaurante', 'bairro do restaurante', restaurant.data.get('id'))
    response = client.patch(f'/restaurant/address/{address.data.get("id")}/', {'line1': 'rua das flores'})
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_address_delete_request(restaurant, address, client):
    restaurant = restaurant('bk', 'fastfood')
    address = address('rua do restaurante', 'bairro do restaurante', restaurant.data.get('id'))
    address_id = address.data.get('id')
    response = client.delete(f'/restaurant/address/{address_id}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_schedule_post_request(restaurant, schedule):
    restaurant = restaurant('bk', 'fastfood')
    restaurant_id = restaurant.data.get('id')
    response = schedule('Quarta', restaurant_id)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_schedule_put_request(client, restaurant, schedule, schedule_info):
    restaurant = restaurant('bk', 'fastfood')
    restaurant_id = restaurant.data.get('id')
    schedule = schedule('Quarta', restaurant_id)
    schedule_data = dict(schedule.data[0])
    schedule_info = schedule_info('Quarta', restaurant_id)[0]
    schedule_info.get('interval_id').update({'open': '10:00:00'})
    response = client.put(f'/restaurant/schedule/{schedule_data.get("id")}/', schedule_info, format='json')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_schedule_patch_request(client, restaurant, schedule):
    restaurant = restaurant('bk', 'fastfood')
    restaurant_id = restaurant.data.get('id')
    schedule = schedule('Quarta', restaurant_id)
    schedule_data = dict(schedule.data[0])
    response = client.patch(f'/restaurant/schedule/{schedule_data.get("id")}/',
                            {'interval_id': {'day': 'Segunda', 'open': '10:00:00', 'close': '16:00:00'},
                             'restaurant_id': restaurant_id}, format='json')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_schedule_delete_request(client, restaurant, schedule):
    restaurant_1 = restaurant('bk', 'fastfood')
    schedule_1 = schedule('Quarta', restaurant_1.data.get('id'))
    restaurant_2 = restaurant('bk shakes', 'sorveteria')
    schedule_2 = schedule('Quarta', restaurant_2.data.get('id'))
    response = client.delete(f'/restaurant/schedule/{dict(schedule_1.data[0]).get("id")}/')
    response_get_restaurant = client.get(f'/restaurant/management/{restaurant_2.data.get("id")}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT and dict(
        response_get_restaurant.data.get('opening_days')[0]).get('interval_id')


@pytest.mark.django_db
def test_contact_post_request(contact, restaurant):
    restaurant = restaurant('bk', 'fastfood')
    contact = contact(restaurant.data.get("id"))
    assert contact.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_contact_put_request(client, restaurant, contact, contact_info):
    restaurant = restaurant('bk', 'fastfood')
    contact = contact(restaurant.data.get("id"))
    data = contact_info(restaurant.data.get("id"))[0]
    data.update({'information': '@bkff'})
    response = client.put(f'/restaurant/contact/{contact.data[0].get("id")}/', data)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_contact_patch_request(client, restaurant, contact):
    restaurant = restaurant('bk', 'fastfood')
    contact = contact(restaurant.data.get("id"))
    response = client.patch(f'/restaurant/contact/{contact.data[0].get("id")}/', {'information': '@bkff'})
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_contact_delete_request(client, restaurant, contact):
    restaurant = restaurant('bk', 'fastfood')
    contact = contact(restaurant.data.get("id"))
    response = client.delete(f'/restaurant/contact/{contact.data[0].get("id")}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT

