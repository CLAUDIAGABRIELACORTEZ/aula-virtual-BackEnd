
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import Docente
from .serializers import DocenteSerializer, DocenteCreateSerializer

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from core.serializers import CursoSerializer, MateriaSerializer
from core.models import CursoMateria
from accounts.permissions import IsDocente
class DocenteViewSet(viewsets.ModelViewSet):  #  ModelViewSet permite POST
    queryset = Docente.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return DocenteCreateSerializer
        return DocenteSerializer

    def create(self, request, *args, **kwargs):
            # Usamos el serializer de creación
            serializer = DocenteCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            docente = serializer.save()

            # Serializamos el resultado con detalles completos
            response_serializer = DocenteSerializer(docente)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class MateriasDelDocenteView(APIView):
    permission_classes = [IsAuthenticated, IsDocente]

    def get(self, request):
        try:
            docente = Docente.objects.get(user=request.user)
        except Docente.DoesNotExist:
            return Response({"error": "No es un docente válido"}, status=403)

        materias = docente.materias.all()
        cursos = {}

        # Buscar las relaciones curso-materia asociadas a esas materias
        for cm in CursoMateria.objects.filter(materia__in=materias).select_related("curso", "materia"):
            curso_id = cm.curso.id
            if curso_id not in cursos:
                cursos[curso_id] = {
                    "curso": CursoSerializer(cm.curso).data,
                    "materias": []
                }
            cursos[curso_id]["materias"].append(MateriaSerializer(cm.materia).data)

        return Response(list(cursos.values()))