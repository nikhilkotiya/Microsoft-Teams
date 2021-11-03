from django.contrib import admin
from django.urls import path, include
# import users
# from test_api import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('',include('chat.urls')),
    path('accounts/',include('allauth.urls')),
    path('private/',include('app1.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)