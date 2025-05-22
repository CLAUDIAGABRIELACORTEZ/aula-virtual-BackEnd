from rest_framework.routers import DefaultRouter 
from django.urls import path
from .views import (
    CursoViewSet,
    MateriaViewSet,
    CursoMateriaViewSet,
    CursoMateriaDocenteViewSet,
    VistaAsignacionesDocente,
)

router = DefaultRouter()
router.register("cursos", CursoViewSet)
router.register("materias", MateriaViewSet)
router.register("cursos-materias", CursoMateriaViewSet)
router.register("asignaciones", CursoMateriaDocenteViewSet)

urlpatterns = router.urls + [
    path("mis-asignaciones/", VistaAsignacionesDocente.as_view(), name="vista_asignaciones_docente"),
]
