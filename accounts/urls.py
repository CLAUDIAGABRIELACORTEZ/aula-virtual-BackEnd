from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet,CurrentUserView

router = DefaultRouter()
router.register(r'usuarios', UserViewSet)

urlpatterns = router.urls
urlpatterns += [
    path('auth/me/', CurrentUserView.as_view(), name='current-user'),
]

