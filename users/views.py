from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from django.contrib import messages

from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from baskets.models import Basket



def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
        else:
            print(form.errors)
    else:
        form = UserLoginForm()
    context = {'title': 'GeekShop - Авторизация', 'form': form}
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Поздравляем! Регистрация прошла успешно!')
            return HttpResponseRedirect(reverse('users:login'))
        else:
            print(form.errors)
    else:
        form = UserRegistrationForm()
    context = {'title': 'GeekShop - Регистрация', 'form': form}
    return render(request, 'users/registration.html', context)


def profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(instance=user, files=request.FILES, data=request.POST)
        name1 = request.POST.get('first_name')
        name2 = request.POST.get('last_name')
        print(name1.isalpha())
        print(name2.isalpha())
        if form.is_valid():
            if name1.isalpha():
                if name2.isalpha():
                    form.save()
                    messages.success(request, 'Изменения внесены!')
                    return HttpResponseRedirect(reverse('users:profile'))
                else:
                    messages.success(request, 'Неправильно введена фамилия')
                    form = UserProfileForm(instance=user)
            else:
                messages.success(request, 'Неправильно введено имя')
                form = UserProfileForm(instance=user)
    else:
        form = UserProfileForm(instance=user)
    context = {'title': 'GeekShop - Профиль',
               'form': form,
               'baskets': Basket.objects.filter(user=user),
               }
    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


