
from django.urls import path
from .views import MateriasDelDocenteView
from rest_framework.routers import DefaultRouter
from .views import DocenteViewSet

router = DefaultRouter()
router.register(r'docentes', DocenteViewSet)

urlpatterns = router.urls + [
    path("docentes/mis-materias/", MateriasDelDocenteView.as_view(), name="materias-del-docente"),
]
