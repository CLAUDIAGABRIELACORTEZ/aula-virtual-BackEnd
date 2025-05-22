from rest_framework import viewsets
from .models import Alumno
from .serializers import AlumnoCreateSerializer, AlumnoDetailSerializer

class AlumnoViewSet(viewsets.ModelViewSet):
    queryset = Alumno.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return AlumnoDetailSerializer
        return AlumnoCreateSerializer

