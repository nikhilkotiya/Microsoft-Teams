from django.contrib import admin
from django.urls import path, include
# import users
# from test_api import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('',include('test_api.urls')),
    path('', include('accounts.urls')),
    # path('feed/',include('blog.urls')),
    path('messages/',include('chat_box.urls')),
    # path('blogapi/',include('blogapi.urls')),
    # path('chat_box/',include('chat_box.urls')),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)