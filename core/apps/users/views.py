from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.http import HttpResponseRedirect, HttpResponse

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.utils.http import urlsafe_base64_decode

from core.apps.library.models import Book  # Book App
from core.apps.users.tokens import TokenGenerator  # User App
from core.apps.users.mixins import OnlyUnauthenticatedMixin
from core.apps.users.forms import UserSignupForm, UserLoginForm, UserEditForm, BookForm

User = get_user_model()


class EditUserDetailsView(LoginRequiredMixin, View):
    template_name = 'accounts/user/edit_details.html'

    def post(self, request, *args, **kwargs):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
        return render(request, self.template_name, {'user_form': user_form})

    def get(self, request, *args, **kwargs):
        user_form = UserEditForm(instance=request.user)
        return render(request, self.template_name, {'user_form': user_form})


class UserDeleteConfirmView(TemplateView, LoginRequiredMixin):
    template_name = 'accounts/user/delete_confirm.html'


class UserDeactivateView(TemplateView):
    template_name = 'accounts/user/delete_user.html'

    def post(self, request):
        user = User.objects.get(username=request.user)
        user.is_active = False
        user.save()
        logout(request)
        return redirect('users:delete_user_confirm')


class AccountSettingsView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'accounts/user/account-settings.html')


class UserAccountEmailConfirmView(TemplateView):
    template_name = 'accounts/registration/register_email_confirm.html'


class UserAccountActivationView(TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            user_id = urlsafe_base64_decode(kwargs['uid']).decode()
            user = User.objects.get(pk=user_id)

            if TokenGenerator.check_token(user, kwargs['token']):
                if not user.is_active:
                    user.is_active = True
                    user.save()
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponse('User is already active!')

            else:
                return HttpResponse('Activation link is invalid!')

        except User.DoesNotExist:
            return HttpResponse('User not found!')

        except (KeyError, TypeError, ValueError):
            return HttpResponse('Error in activation!')


class UserSignupView(CreateView, OnlyUnauthenticatedMixin):
    template_name = 'accounts/registration/signup.html'
    form_class = UserSignupForm
    success_url = reverse_lazy('users:confirm-email')

    def get_form_kwargs(self):
        """Send request to the form."""
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class UserLoginView(LoginView):
    template_name = 'accounts/registration/login.html'
    success_url = reverse_lazy('library:books_home')
    form_class = UserLoginForm

    def form_valid(self, form):
        print(form.cleaned_data)
        email = form.cleaned_data['username']  # This is an email field
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, 'Invalid login credentials')
            return self.form_invalid(form)


class UserLogoutView(LoginRequiredMixin, LogoutView, SuccessMessageMixin):
    success_message = 'You have been logged out.'

    def get_success_url(self):
        return reverse_lazy('library:books_home')


class BookUploadView(CreateView):
    form_class = BookForm
    template_name = 'accounts/up.html'

    def get_form_kwargs(self):
        """Send request to the form."""
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class FavoriteListView(View, LoginRequiredMixin):

    def get(self, request, *args, **kwargs):
        user = request.user
        books = Book.objects.filter(favorites=user)
        return render(request, 'accounts/user/add_to_favorite.html', {
            'favorite': books,
        })


class AddToFavoriteView(View, LoginRequiredMixin):
    def get(self, request, bid, *args, **kwargs):  # bid => book id
        book = get_object_or_404(Book, id=bid)
        if book.favorites.filter(id=request.user.id).exists():
            book.favorites.remove(request.user)
            messages.success(request, f"{book.title} is removed from your favorites.")
        else:
            book.favorites.add(request.user)
            messages.success(request, f"{book.title} is added to your favorites.")

        return HttpResponseRedirect(request.META['HTTP_REFERER'])
