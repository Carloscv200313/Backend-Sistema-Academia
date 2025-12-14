from rest_framework import serializers
from .models import *

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class ApoderadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apoderado
        fields = '__all__'

class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = '__all__'

class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = '__all__'

class DocenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Docente
        fields = '__all__'

class CicloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ciclo
        fields = '__all__'

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'

class CicloCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CicloCurso
        fields = '__all__'

class AlumnoCicloCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlumnoCicloCurso
        fields = '__all__'

class SimulacroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Simulacro
        fields = '__all__'

class SimulacroAlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimulacroAlumno
        fields = '__all__'

class HorarioCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HorarioCurso
        fields = '__all__'

class AsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asistencia
        fields = '__all__'
