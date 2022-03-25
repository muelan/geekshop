from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import auth
from django.shortcuts import render, HttpResponseRedirect
from users.models import User
# from django.contrib import messages

from common.views import CommonContextMixin
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from users.models import User
from baskets.models import Basket


class UserLoginView(CommonContextMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'GeekShop - Авторизация'


class UserRegistrationView(CommonContextMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегестрировались!'
    title = 'GeekShop - Регистрация'

    def send_verify_mail(self, user):
        verify_link = reverse('users:verify', args=[user.email, user.activation_key])
        title = f'Подтверждение учетной записи {user.username}'
        message = f'Для подтверждения учетной записи {user.username} на портале ' \
                  f'{settings.DOMAIN_NAME} перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'
        return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    def get_context_data(self, **kwargs):
        title = 'GeekShop - Регистрация'
        context = super(UserRegistrationView, self).get_context_data(**kwargs)
        context.update(
            title=title,
            register_form=self.form_class()
        )
        return context

    def post(self, request, *args, **kwargs):
        title = 'GeekShop - Регистрация'
        register_form = UserRegistrationForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save()
            if self.send_verify_mail(user):
                print('Сообщение подтверждения отправлено')
                return HttpResponseRedirect(reverse('users:login'))
            else:
                print('Ошибка отправки сообщения')
                return HttpResponseRedirect(reverse('users:login'))
        else:
            register_form = UserRegistrationForm()
            content = {'title': title, 'register_form': register_form}
            return render(request, 'users/registration.html', content)


def verify(request, email, activate_key):
    try:
        user = User.objects.get(email=email)
        if user and user.activation_key == activate_key and not user.is_activation_key_expired:
            user.activation_key = ''
            user.activation_key_expires = None
            user.is_active = True
            user.save(update_fields=['activation_key', 'activation_key_expires', 'is_active'])
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'users/verification.html')
        else:
            print(f'Ошибка активации пользователя: {user}')
            return render(request, 'users/verification.html')
    except Exception as e:
        print(f'Ошибка активации пользователя : {e.args}')
        return HttpResponseRedirect(reverse('IndexView'))


class UserProfileView(CommonContextMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'GeekShop - Личный кабинет'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['baskets'] = Basket.objects.filter(user=self.object)
        return context


class UserLogoutView(LogoutView):
    pass






# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user and user.is_active:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#         else:
#             print(form.errors)
#     else:
#         form = UserLoginForm()
#     context = {'title': 'GeekShop - Авторизация', 'form': form}
#     return render(request, 'users/login.html', context)
#
#
# def registration(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Поздравляем! Регистрация прошла успешно!')
#             return HttpResponseRedirect(reverse('users:login'))
#         else:
#             print(form.errors)
#     else:
#         form = UserRegistrationForm()
#     context = {'title': 'GeekShop - Регистрация', 'form': form}
#     return render(request, 'users/registration.html', context)
#
#
# @login_required
# def profile(request):
#     user = request.user
#     if request.method == 'POST':
#         form = UserProfileForm(instance=user, files=request.FILES, data=request.POST)
#         name1 = request.POST.get('first_name')
#         name2 = request.POST.get('last_name')
#         if form.is_valid():
#             if name1.isalpha():
#                 if name2.isalpha():
#                     form.save()
#                     messages.success(request, 'Изменения внесены!')
#                     return HttpResponseRedirect(reverse('users:profile'))
#                 else:
#                     messages.success(request, 'Неправильно введена фамилия')
#                     form = UserProfileForm(instance=user)
#             else:
#                 messages.success(request, 'Неправильно введено имя')
#                 form = UserProfileForm(instance=user)
#     else:
#         form = UserProfileForm(instance=user)
#     context = {'title': 'GeekShop - Профиль',
#                'form': form,
#                'baskets': Basket.objects.filter(user=user),
#                }
#     return render(request, 'users/profile.html', context)
#
#
# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))


# class CommonContextMixin:
#     title = None
#
#     def get_context_data(self, **kwargs):
#         context = super(CommonContextMixin, self).get_context_data(**kwargs)
#         context['title'] = self.title
#         return context


