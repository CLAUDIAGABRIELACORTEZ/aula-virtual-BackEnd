from rest_framework.routers import DefaultRouter
from .views import EvaluacionActividadViewSet, NotaActividadViewSet, AutoevaluacionViewSet
# from .views import ResumenNotasView
from django.urls import path
from .views import ListaAlumnosMateriaView
from .views import CuadriculaNotasView

from .views import PrediccionTrim3View

router = DefaultRouter()
router.register(r'actividades', EvaluacionActividadViewSet)
router.register(r'notas-actividad', NotaActividadViewSet)
router.register(r'autoevaluaciones', AutoevaluacionViewSet)


urlpatterns = router.urls
urlpatterns += [
    # path("resumen/", ResumenNotasView.as_view(), name="resumen-notas"),
    path("alumnos-materia/", ListaAlumnosMateriaView.as_view(), name="alumnos_por_materia"),
    path("cuadricula/", CuadriculaNotasView.as_view(), name="cuadricula-notas"),
    path("prediccion-trim3/", PrediccionTrim3View.as_view(), name="prediccion-trim3")
    
]