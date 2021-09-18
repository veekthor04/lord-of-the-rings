from django.urls import path

from .views import CreateUserView, CreateTokenView, ProfileUserView

app_name = 'user'

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('token/', CreateTokenView.as_view(), name='token'),
    path('profile/', ProfileUserView.as_view(), name='profile')
]
