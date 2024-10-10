from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user.views import register, home, login, logout, CustomAuthToken, UserRegister

router = DefaultRouter()
router.register(r'register_user', UserRegister)

urlpatterns = [
    path('user/', include(router.urls)),
    path('home/', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('api/token/', CustomAuthToken.as_view(), name='token_obtain')
]