from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.http import HttpResponseRedirect, HttpResponse

from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, TemplateView, DeleteView, ListView, UpdateView

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.utils.http import urlsafe_base64_decode

from core.apps.library.models import Book  # Book App
from core.apps.users.tokens import TokenGenerator  # User App
from core.apps.users.mixins import OnlyUnauthenticatedMixin
from core.apps.users.forms import UserSignupForm, UserLoginForm, UserEditForm, BookForm

User = get_user_model()


class EditUserDetailsView(LoginRequiredMixin, UpdateView):
    """ View for editing user details. """

    form_class = UserEditForm
    template_name = 'accounts/user/edit_details.html'
    success_url = reverse_lazy("users:edit_details")

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserEditForm(instance=self.request.user)
        return context


class UserDeleteConfirmView(TemplateView, LoginRequiredMixin):
    template_name = 'accounts/user/delete_confirm.html'


class UserDeactivateView(DeleteView):
    """  View for deactivating a user account. """

    template_name = 'accounts/user/delete_user.html'
    success_url = reverse_lazy('users:delete_user_confirm')

    def get_object(self, queryset=None):
        """Returns the current user as the object to be deactivated."""
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.save()
        logout(request)
        return super().delete(request, *args, **kwargs)


class AccountSettingsView(TemplateView, LoginRequiredMixin):
    template_name = 'accounts/user/account-settings.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        return super(AccountSettingsView, self).dispatch(request, *args, **kwargs)


class UserAccountEmailConfirmView(TemplateView):
    template_name = 'accounts/registration/register_email_confirm.html'


class UserAccountActivationView(TemplateView):
    """  View for user account activation. """

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
    """ Custom user login view. """

    form_class = UserLoginForm
    success_url = reverse_lazy('library:books_home')
    template_name = 'accounts/registration/login.html'

    def form_valid(self, form):
        email = form.cleaned_data['username']  # This is an email field
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, 'Invalid login credentials')
            return self.form_invalid(form)


class UserLogoutView(LoginRequiredMixin, SuccessMessageMixin, LogoutView):
    success_message = 'You have been logged out.'
    success_url = reverse_lazy('Library:books_home')

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


class FavoriteListView(LoginRequiredMixin, ListView):
    model = Book
    context_object_name = 'favorite'
    template_name = 'accounts/user/add_to_favorite.html'

    def get_queryset(self):
        user = self.request.user
        return Book.objects.filter(favorites=user)


class AddToFavoriteView(View, LoginRequiredMixin):
    """ View for adding or removing a book from the user's favorites. """

    def get(self, request, book_id, *args, **kwargs):

        book = get_object_or_404(Book, id=book_id)
        user = request.user
        
        if book.favorites.filter(id=user.id).exists():
            book.favorites.remove(user)
            action = 'removed from'

        else:
            book.favorites.add(user)
            action = 'added to'

        messages.success(request, f"{book.title} is {action} your favorites.")
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
