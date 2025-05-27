# students/serializers.py

from rest_framework import serializers
from .models import Alumno
from core.models import Curso, Materia
from accounts.models import CustomUser

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "username", "nombre", "apellido", "ci", "telefono", "rol"]

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ["id", "nombre", "nivel"]

class MateriaSerializer(serializers.ModelSerializer):
    curso = CursoSerializer()

    class Meta:
        model = Materia
        fields = ["id", "nombre", "curso"]

# class AlumnoDetailSerializer(serializers.ModelSerializer):
#     user = SimpleUserSerializer()
#     curso = CursoSerializer()
#     # materias = MateriaSerializer(many=True)

#     # class Meta:
#     #     model = Alumno
#     #     fields = ["id", "user", "curso", "materias"]
#     materias = serializers.SerializerMethodField()

#     def get_materias(self, obj):
#         if obj.curso:
#             return MateriaSerializer(obj.curso.materias.all(), many=True).data
#         return []
class AlumnoDetailSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()
    curso = CursoSerializer()
    # materias = serializers.SerializerMethodField()

    class Meta:
        model = Alumno
        fields = ["id", "user", "curso"]

    def get_materias(self, obj):
        if obj.curso:
            return MateriaSerializer(obj.curso.materias.all(), many=True).data
        return []

class AlumnoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = ['user', 'curso']  # No incluimos 'materias' aquí

    def create(self, validated_data):
        from core.models import Materia  # Import dentro del método para evitar posibles import circular

        alumno = Alumno.objects.create(**validated_data)

        # # Asignar todas las materias del sistema al nuevo alumno
        # todas_las_materias = Materia.objects.all()
        # alumno.materias.set(todas_las_materias)

        return alumno
