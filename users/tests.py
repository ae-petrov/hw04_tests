from django.test import Client, TestCase
from django.core import mail


class ProfileTest(TestCase):

    def test_registration_and_send_email(self):
        password = '!q2w3e4r5t'

        self.client.post('/auth/signup/', {'username':'rocketman', 'email':'rocketman@fly.co.uk', 'password1':password, 'password2':password})
        self.assertEqual(len(mail.outbox), 1, 'Проверьте, что почта отправляется.')
        self.assertEqual(mail.outbox[0].subject, 'Подтверждение регистрации пользователя rocketman', 'Тема письма не соответсвует шаблону')


    def test_profile_page_created(self):
        username = 'rocketman'
        password = '!q2w3e4r5t'

        self.client.post('/auth/signup/', {'username':username, 'email':'rocketman@fly.co.uk', 'password1':password, 'password2':password})
        response = self.client.get(f'/{username}/')
        self.assertEqual(response.status_code, 200)