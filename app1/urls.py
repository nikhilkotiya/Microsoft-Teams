from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import Inbox, UserSearch, Directs, NewConversation, SendDirect
urlpatterns = [
   	path('', Inbox, name='inbox'),
   	path('directs/m/<email>', Directs, name='directs'),
   	path('new/', UserSearch, name='usersearch'),
   	path('new/<email>', NewConversation, name='newconversation'),
   	path('send/<email>/', SendDirect, name='send_direct'),
	path('send/', SendDirect, name='send_direct'),
    #path('send/', views.SendMessageView.as_view(), name="send_message"),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)