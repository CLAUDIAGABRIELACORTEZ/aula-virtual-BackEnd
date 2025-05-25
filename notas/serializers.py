from rest_framework import serializers
from .models import EvaluacionActividad, NotaActividad, Autoevaluacion
from accounts.models import CustomUser


class EvaluacionActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluacionActividad
        fields = ['id', 'curso', 'materia', 'trimestre', 'dimension', 'descripcion', 'fecha']


class NotaActividadSerializer(serializers.ModelSerializer):
    alumno_nombre = serializers.SerializerMethodField()

    class Meta:
        model = NotaActividad
        fields = ['id', 'evaluacion', 'alumno', 'alumno_nombre', 'nota']

    def get_alumno_nombre(self, obj):
        return f"{obj.alumno.nombre} {obj.alumno.apellido}"


class AutoevaluacionSerializer(serializers.ModelSerializer):
    alumno_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Autoevaluacion
        fields = ['id', 'curso', 'materia', 'alumno', 'alumno_nombre', 'trimestre', 'nota']

    def get_alumno_nombre(self, obj):
        return f"{obj.alumno.nombre} {obj.alumno.apellido}"
