
from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

#Nuevo de Rodrigo
from students.models import Alumno
from core.models import Materia

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # 👈 añadir explícitamente

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "username",
            "nombre",
            "apellido",
            "ci",
            "telefono",
            "rol",
            "password",  # 👈 asegúrate de incluirlo aquí
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Agregamos más info personalizada al token
        data['rol'] = self.user.rol
        data['username'] = self.user.username
        data['email'] = self.user.email

        #data['user_id'] = self.user.id

        # Si es alumno, agregar curso y materias
        try:
            alumno = Alumno.objects.select_related('curso').get(user=self.user)

            data['alumno_id'] = alumno.id #id del alumno

            data['curso'] = {
                "id": alumno.curso.id,
                "nombre": alumno.curso.nombre,
                "nivel": alumno.curso.nivel
            }

            materias = alumno.curso.materias.all()
            data['materias'] = [{"id": m.id, "nombre": m.nombre} for m in materias]
        except Alumno.DoesNotExist:
            pass

        return data
 