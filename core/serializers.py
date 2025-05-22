
from rest_framework import serializers
from .models import Curso, Materia, CursoMateria
from rest_framework import serializers
from accounts.models import CustomUser
from .models import CursoMateriaDocente

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ["id", "nombre", "nivel"]

class MateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materia
        fields = ["id", "nombre"]

# Serializer para asignar materias a cursos
class CursoMateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CursoMateria
        fields = ["id", "curso", "materia"]


class DocenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "nombre", "apellido", "email"]

class CursoMateriaDetailSerializer(serializers.ModelSerializer):
    curso = CursoSerializer()
    materia = MateriaSerializer()

    class Meta:
        model = CursoMateria
        fields = ["id", "curso", "materia"]

class CursoMateriaDocenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CursoMateriaDocente
        fields = ["id", "curso", "materia", "docente"]


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ["id", "nombre", "nivel"]

class MateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materia
        fields = ["id", "nombre"]

class DocenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "nombre", "apellido", "email"]

        
class CursoMateriaDocenteDetailSerializer(serializers.ModelSerializer):
    curso = CursoSerializer()
    materia = MateriaSerializer()
    docente = DocenteSerializer()

    class Meta:
        model = CursoMateriaDocente
        fields = ["id", "curso", "materia", "docente"]

# par la vista de los Docentes
class AsignacionDocenteSerializer(serializers.ModelSerializer):
    curso = CursoSerializer()
    materia = MateriaSerializer()

    class Meta:
        model = CursoMateriaDocente
        fields = ["curso", "materia"]
