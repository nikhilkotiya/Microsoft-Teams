from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
# User login and logout with default Django views
from . views import SignUpView
urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path('',views.home,name='home'),
    path('accounts/logout/',views.ulogout,name="logout"), 
    path('accounts/login/', views.login_view, name='login'),
   path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # path('accounts/signup/', views.signup, name='signup'),
]  