from django.urls import path
# from .views import send_test_email, send_advanced_email, home
from .views import home

urlpatterns = [
    path('', home), 
    # path('text/', send_test_email),
    # path('file/', send_advanced_email)

]