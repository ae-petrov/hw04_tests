from django.shortcuts import render
from django.views.generic import CreateView
from django.core import mail
from django.http import HttpResponse

from .forms import CreationForm

class SignUp(CreateView):
    form_class = CreationForm
    success_url = '/auth/login/'
    template_name = 'signup.html'

    def form_valid(self, form):
        to_email = form.cleaned_data.get("email")
        new_user = form.cleaned_data.get("username")
        send_confirmation(to_email, new_user)
        return super().form_valid(form)


def send_confirmation(to_email, new_user):
    subject, from_email, to = f'Подтверждение регистрации пользователя {new_user}', 'noreply@yatube.app', to_email
    text_content = f'Вы (или кто-то другой) были зарегистрированны на сайте yatube. Поздравляем! Имя пользователя {new_user}'
    mail.send_mail(subject, text_content, from_email, [to], fail_silently=False)

# Create your views here.
