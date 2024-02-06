from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from core.apps.users import views
from .forms import PasswdResetConfirmForm, PasswdResetForm

app_name = 'users'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('signup/', views.UserSignupView.as_view(), name='signup'),
    path('confirm-email/', views.UserAccountEmailConfirmView.as_view(), name='confirm-email'),
    path('activate/<uid>/<token>/', views.UserAccountActivationView.as_view(), name='activate'),

    # Password reset URLs
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset/password_reset_form.html',
        email_template_name='accounts/password_reset/password_reset_email.html',
        success_url='password-reset-email-confirm/',
        form_class=PasswdResetForm
    ), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset/password_reset_confirm.html',
        success_url='/password-reset-complete/',
        form_class=PasswdResetConfirmForm
    ), name='password_reset_confirm'),
    path('password-reset/password-reset-email-confirm/',
         TemplateView.as_view(template_name="accounts/password_reset/reset_status.html"),
         name='password_reset_done'),
    path('password-reset/password-reset-complete/',
         TemplateView.as_view(template_name="accounts/password_reset/reset_status.html"),
         name='password_reset_complete'),

    # User profile URLs
    path('profile/edit/', views.EditUserDetailsView.as_view(), name='edit_details'),
    path('profile/deactivate/', views.UserDeactivateView.as_view(), name='delete_user'),
    path('profile/delete-confirm/', views.UserDeleteConfirmView.as_view(), name='delete_user_confirm'),
    path('accounts-settings/', views.AccountSettingsView.as_view(), name='accounts-settings'),
    path('upload-book/', views.BookUploadView.as_view(), name='upload-book'),

    # Favorite List URLs
    path('favorite/', views.FavoriteListView.as_view(), name='favorite'),
    path('favorite/add-to-favorite/<int:bid>', views.AddToFavoriteView.as_view(), name='add_to_favorite'),

]
