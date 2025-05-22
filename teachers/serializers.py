
from rest_framework import serializers
from .models import Docente
from core.models import Materia
from accounts.models import CustomUser

# Subserializer para materias
class MateriaSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materia
        fields = ['id', 'nombre']

# Subserializer para usuario
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'nombre','apellido', 'ci', 'telefono']

# Serializer principal para docente
class DocenteSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    # materias = MateriaSimpleSerializer(many=True)

    class Meta:
        model = Docente
        fields = ['id', 'user']

class DocenteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Docente
        fields = ['user']

    # def update(self, instance, validated_data):
    #     # Actualizar usuario (ya lo haces aparte en el frontend)
    #     materias = validated_data.pop('materias', None)
    #     if materias is not None:
    #         instance.materias.set(materias)  # actualiza las materias
    #     instance.save()
    #     return instance

