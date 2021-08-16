from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

UserModel = get_user_model()


class ProfileTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_register_and_save_user_in_db(self):
        before_save = UserModel.objects.count()
        UserModel.objects.create_user(email='peter@abv.bg', password='123')
        after_save = UserModel.objects.count()
        self.assertEqual(before_save + 1, after_save)

    def test_get_details_when_loggedIn_should_getDetails(self):
        user = UserModel.objects.create_user(email='peter@abv.bg', password='123')
        self.client.force_login(user)
        response = self.client.get(reverse('profile'))
        self.assertEqual(user.id, response.context['profile'].user_id)
        self.assertEqual(200, response.status_code)

    def test_delete_and_remove_user_from_db(self):
        UserModel.objects.create_user(email='peter@abv.bg', password='123')
        before_delete = UserModel.objects.count()
        UserModel.objects.first().delete()
        after_delete = UserModel.objects.count()
        self.assertEqual(before_delete - 1, after_delete)

    def test_profilesList_getDetails_whenSuperUser_withNOOtherUsersCreated(self):
        user = UserModel.objects.create_superuser(email='peter@abv.bg', password='123')
        self.client.force_login(user)
        response = self.client.get(reverse('all profiles'))
        self.assertEqual(len(list(response.context['profiles'])), len([user]))

    def test_profilesList_getDetails_whenSuperUser_withOtherUsersCreated(self):
        user = UserModel.objects.create_superuser(email='peter@abv.bg', password='123')
        self.client.force_login(user)
        test_user1 = UserModel.objects.create_user(email='test@abv.bg', password='test')
        response = self.client.get(reverse('all profiles'))
        self.assertNotEqual(len(list(response.context['profiles'])), len([user]))
