from django.test import Client, TestCase
from django.core import mail

from .models import User

class PostTest(TestCase):

    def test_create_new_post(self):
        username = 'rocketman'
        password = '!q2w3e4r5t'
        new_post = 'Самый короткий пост'

        self.client.post('/auth/signup/', {'username':username, 'email':'rocketman@fly.co.uk', 'password1':password, 'password2':password})
        response = self.client.login(username=username, password=password)
        self.assertTrue(response, f'Пользователь {username} не может быть залогинен')

        response = self.client.post('/new/', {'group':'', 'text':new_post}, follow=True)
        self.assertTupleEqual(('/', 302), (tuple(response.redirect_chain)[0]), 'Проверьте что пользователь перенаправлен на главную страницу после создания поста')
        self.assertContains(response, new_post, 1, 200, 'Текст нового поста не найден на главной странице поста')
        
        for url in ('/', f'/{username}/'):
            response = self.client.get(url)
            self.assertEqual(1, len(response.context['page']), f'Проверьте отображается ли вновь опубликованный пост на странице: {url}')
            self.assertContains(response, new_post, 1, 200, f'Текст нового поста не найден на странице: {url}')

        response = self.client.get(f'/{username}/1/')
        self.assertContains(response, new_post, 1, 200, 'Текст нового поста не найден на странице просмотра поста')


    def test_try_anonymous_create_new_post(self):
        response = self.client.get('/new/', follow=True)
        self.assertTupleEqual(('/auth/login/?next=/new/', 302), (tuple(response.redirect_chain)[0]))


    def test_edit_post(self):
        username = 'rocketman'
        password = '!q2w3e4r5t'
        new_post = 'Самый короткий'
        edited_post = 'Другой пост'

        self.client.post('/auth/signup/', {'username':username, 'email':'rocketman@fly.co.uk', 'password1':password, 'password2':password})
        self.client.login(username=username, password=password)

        response = self.client.post('/new/', {'group': '', 'text': new_post}, follow=True)
        for url in ('/', f'/{username}/', f'/{username}/1/'):
            response = self.client.get(url)
            self.assertContains(response, new_post)

        response = self.client.post(f'/{username}/1/edit/', {'group':'', 'text':edited_post}, follow=True)
        self.assertEqual(response.status_code, 200)
        for url in ('/', f'/{username}/', f'/{username}/1/'):
            response = self.client.get(url)
            self.assertContains(response, edited_post, 1, 200, f'Проверьте наличие поста на странице: {url}')