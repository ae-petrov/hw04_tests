#from unittest import TestCase
from django.test import Client, TestCase
from django.core import mail

from .models import User

class ProfileTest(TestCase):

    def test_registrationAndSendEmail(self):
        pswrd = '!q2w3e4r5t'

        self.client.post('/auth/signup/', {'username':'rocketman', 'email':'rocketman@fly.co.uk', 'password1':pswrd, 'password2':pswrd})
        self.assertEqual(len(mail.outbox), 1, 'Проверьте, что почта отправляется.')
        self.assertEqual(mail.outbox[0].subject, 'Подтверждение регистрации пользователя rocketman', 'Тема письма не соответсвует шаблону')


    def test_profilePageCreated(self):
        username = 'rocketman'
        pswrd = '!q2w3e4r5t'

        self.client.post('/auth/signup/', {'username':username, 'email':'rocketman@fly.co.uk', 'password1':pswrd, 'password2':pswrd})
        response = self.client.get(f'/{username}/')
        self.assertEqual(response.status_code, 200)


class PostTest(TestCase):

    def test_createNewPost(self):
        username = 'rocketman'
        pswrd = '!q2w3e4r5t'
        new_post = 'Самый короткий пост'

        self.client.post('/auth/signup/', {'username':username, 'email':'rocketman@fly.co.uk', 'password1':pswrd, 'password2':pswrd})
        response = self.client.login(username=username, password=pswrd)
        self.assertTrue(response, f'Пользователь {username} не может быть залогинен')

        response = self.client.post('/new/', {'group':'', 'text':new_post}, follow=True)
        self.assertTupleEqual((f'/{username}/1/', 302), (tuple(response.redirect_chain)[0]), 'Проверьте доступность поста на странице просмотра поста')
        self.assertContains(response, new_post, 1, 200, 'Текст нового поста не найден на странице просмотра поста')
        
        for url in ('/', f'/{username}/'):
            response = self.client.get(url)
            self.assertEqual(1, len(response.context['page']), f'Проверьте отображается ли вновь опубликованный пост на странице: {url}')
            self.assertContains(response, new_post)


    def test_tryAnonymousCreateNewPost(self):
        response = self.client.get('/new/', follow=True)
        self.assertTupleEqual(('/auth/login/?next=/new/', 302), (tuple(response.redirect_chain)[0]))

    def test_editPost(self):
        username = 'rocketman'
        pswrd = '!q2w3e4r5t'
        new_post = 'Самый короткий'
        edited_post = 'Другой пост'

        self.client.post('/auth/signup/', {'username':username, 'email':'rocketman@fly.co.uk', 'password1':pswrd, 'password2':pswrd})
        self.client.login(username=username, password=pswrd)

        response = self.client.post('/new/', {'group': '', 'text': new_post}, follow=True)
        for url in ('/', f'/{username}/', f'/{username}/1/'):
            response = self.client.get(url)
            self.assertContains(response, new_post)

        response = self.client.post(f'/{username}/1/edit/', {'group':'', 'text':edited_post}, follow=True)
        self.assertEqual(response.status_code, 200)
        for url in ('/', f'/{username}/', f'/{username}/1/'):
            response = self.client.get(url)
            self.assertContains(response, edited_post, 1, 200, f'Проверьте наличие поста на странице: {url}')