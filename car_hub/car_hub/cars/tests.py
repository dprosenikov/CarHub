from datetime import datetime
from random import randint, choice

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse

from car_hub.cars.models import CarModel, LikeModel, CommentModel
from car_hub.cars.validators import validate_year_range

UserModel = get_user_model()


class ValidateYearRangeTest(TestCase):
    def test_when_value_is_within_range(self):
        current_year = datetime.now().year
        value = randint(1886, current_year)
        self.assertIsNone(validate_year_range(value))

    def test_when_value_is_NOT_within_range(self):
        end = datetime.now().year
        valid_range = range(1886, end)
        invalid_range = [el for el in range(1, 5000) if el not in valid_range]
        value = choice(invalid_range)
        with self.assertRaises(ValidationError):
            validate_year_range(value)


class CarsListTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_carList_withNoCars(self):
        user = UserModel.objects.create_user(email='peter@abv.bg', password='123')
        self.client.force_login(user)
        response = self.client.get(reverse('car list'))
        self.assertListEqual(list(response.context['cars']), [])

    def test_carList_withCars(self):
        user = UserModel.objects.create_user(email='peter@abv.bg', password='123')
        self.client.force_login(user)

        car = CarModel.objects.create(
            brand='MercedesBenz',
            description='Car Description',
            year=2000,
            image='https://www.focus2move.com/wp-content/uploads/2020/08/Tesla-Roadster-2020-1024-03.jpg',
            price=24000,
            user=user
        )
        response = self.client.get(reverse('car list'))
        self.assertListEqual(list(response.context['cars']), [car])


class CarsDetailsTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = UserModel.objects.create_user(email='peter@abv.bg', password='123')
        self.client.force_login(self.user)

    def test_owner_and_liked(self):
        car = CarModel.objects.create(
            brand='MercedesBenz',
            description='Car Description',
            year=2000,
            image='https://www.focus2move.com/wp-content/uploads/2020/08/Tesla-Roadster-2020-1024-03.jpg',
            price=24000,
            user=self.user
        )
        like = LikeModel.objects.create(
            car=car,
            user=self.user
        )
        response = self.client.get(reverse('car details', kwargs={
            'pk': car.id,
        }))
        self.assertTrue(response.context['is_owner'])
        self.assertTrue(response.context['is_liked'])

    def test_owner_and_not_liked(self):
        car = CarModel.objects.create(
            brand='MercedesBenz',
            description='Car Description',
            year=2000,
            image='https://www.focus2move.com/wp-content/uploads/2020/08/Tesla-Roadster-2020-1024-03.jpg',
            price=24000,
            user=self.user
        )
        response = self.client.get(reverse('car details', kwargs={
            'pk': car.id,
        }))
        self.assertTrue(response.context['is_owner'])
        self.assertFalse(response.context['is_liked'])

    def test_not_owner_and_liked(self):
        car_user = UserModel.objects.create_user(email='car@user.com', password='123')
        car = CarModel.objects.create(
            brand='MercedesBenz',
            description='Car Description',
            year=2000,
            image='https://www.focus2move.com/wp-content/uploads/2020/08/Tesla-Roadster-2020-1024-03.jpg',
            price=24000,
            user=car_user
        )
        like = LikeModel.objects.create(
            car=car,
            user=self.user
        )
        response = self.client.get(reverse('car details', kwargs={
            'pk': car.id,
        }))
        self.assertFalse(response.context['is_owner'])
        self.assertTrue(response.context['is_liked'])

    def test_not_owner_and_not_liked(self):
        car_user = UserModel.objects.create_user(email='car@user.com', password='123')
        car = CarModel.objects.create(
            brand='MercedesBenz',
            description='Car Description',
            year=2000,
            image='https://www.focus2move.com/wp-content/uploads/2020/08/Tesla-Roadster-2020-1024-03.jpg',
            price=24000,
            user=car_user
        )
        response = self.client.get(reverse('car details', kwargs={
            'pk': car.id,
        }))
        self.assertFalse(response.context['is_owner'])
        self.assertFalse(response.context['is_liked'])

    def test_user_gets_only_owned_cars_at_mycars(self):
        car_user = UserModel.objects.create_user(email='car@user.com', password='123')
        car1 = CarModel.objects.create(
            brand='MercedesBenz',
            description='Car Description',
            year=2000,
            image='https://www.focus2move.com/wp-content/uploads/2020/08/Tesla-Roadster-2020-1024-03.jpg',
            price=24000,
            user=car_user
        )
        car2 = CarModel.objects.create(
            brand='MercedesBenz',
            description='Car Description2',
            year=2000,
            image='https://www.focus2move.com/wp-content/uploads/2020/08/Tesla-Roadster-2020-1024-03.jpg',
            price=24000,
            user=self.user
        )
        own_cars = CarModel.objects.filter(user_id=self.user.id)
        response = self.client.get(reverse('my cars'))
        self.assertEqual(len(response.context['page_obj']), len(own_cars))

        response2 = self.client.get(reverse('car list'))
        self.assertNotEqual(len(response2.context['page_obj']), len(own_cars))


class LikeViewTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = UserModel.objects.create_user(email='peter@abv.bg', password='123')
        self.car_user = UserModel.objects.create_user(email='car@user.com', password='123')
        self.car = CarModel.objects.create(
            brand='MercedesBenz',
            description='Car Description',
            year=2000,
            image='https://www.focus2move.com/wp-content/uploads/2020/08/Tesla-Roadster-2020-1024-03.jpg',
            price=24000,
            user=self.car_user
        )

    def test_like_whenNotLiked(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('like car', kwargs={
            'pk': self.car.id,
        }))
        self.assertEqual(302, response.status_code)
        like_exists = LikeModel.objects.filter(car_id=self.car.id, user_id=self.user.id).exists()
        self.assertTrue(like_exists)

    def test_likePet__whenPetAlreadyLiked_shouldDeleteTheLike(self):
        self.client.force_login(self.user)
        like = LikeModel.objects.create(
            car=self.car,
            user=self.user
        )
        response = self.client.post(reverse('like car', kwargs={
            'pk': self.car.id,
        }))
        self.assertEqual(302, response.status_code)
        like_exists = LikeModel.objects.filter(car_id=self.car.id, user_id=self.user.id).exists()
        self.assertFalse(like_exists)


class CommentAddedTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = UserModel.objects.create_user(email='peter@abv.bg', password='123')

    def test_comment_added(self):
        self.client.force_login(self.user)
        car = CarModel.objects.create(
            brand='MercedesBenz',
            description='Car Description',
            year=2000,
            image='https://www.focus2move.com/wp-content/uploads/2020/08/Tesla-Roadster-2020-1024-03.jpg',
            price=24000,
            user=self.user
        )
        response = self.client.post(reverse('comment car', kwargs={'pk': car.id, }), {'comment': 'Test Comment'})
        self.assertEqual(302, response.status_code)
        comment_exists = CommentModel.objects.filter(car_id=car.id, user_id=self.user.id).exists()
        self.assertTrue(comment_exists)


class CreateEdtiDeleteCarTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = UserModel.objects.create_user(email='peter@abv.bg', password='123')
        self.client.force_login(self.user)
        self.car = CarModel.objects.create(
            brand='MercedesBenz',
            description='Car Description',
            year=2000,
            image='https://www.focus2move.com/wp-content/uploads/2020/08/Tesla-Roadster-2020-1024-03.jpg',
            price=24000,
            user=self.user
        )

    def test_create_car(self):
        response = self.client.get(reverse('create car'))
        self.assertEqual(response.status_code, 302)
        self.car.full_clean()
        self.car.save()
        self.assertIsNotNone(self.car)

    def test_edit_car(self):
        self.car.brand = 'RollsRoyce'
        self.car.description = 'description'
        self.car.year = 1900
        self.car.price = 200
        self.car.full_clean()
        self.car.save()
        edited_car = CarModel.objects.get(pk=self.car.id)
        self.assertEqual(edited_car.brand, 'RollsRoyce')
        self.assertEqual(edited_car.description, 'description')
        self.assertEqual(edited_car.year, 1900)
        self.assertEqual(edited_car.price, 200)

    def test_delete_car(self):
        self.client.delete(reverse('delete car', kwargs={'pk': self.car.id, }))
        self.assertTrue(CarModel.objects.count() == 0)


class SearchTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = UserModel.objects.create_user(email='peter@abv.bg', password='123')
        self.car = CarModel.objects.create(
            brand='Audi',
            description='Car Description',
            year=2000,
            image='https://www.focus2move.com/wp-content/uploads/2020/08/Tesla-Roadster-2020-1024-03.jpg',
            price=24000,
            user=self.user
        )

    def test_search_returns_result(self):
        search = 'Aud'
        cars = CarModel.objects.filter(brand__contains=search)
        response = self.client.post(reverse('search cars'), {'searched_by': search, 'cars': self.car})
        self.assertEqual(len(list(response.context['cars'])), 1)

    def test_search_returns_NO_result(self):
        search = 'test'
        cars = CarModel.objects.filter(brand__contains=search)
        response = self.client.post(reverse('search cars'), {'searched_by': search, 'cars': self.car})
        self.assertNotEqual(len(list(response.context['cars'])), 1)
