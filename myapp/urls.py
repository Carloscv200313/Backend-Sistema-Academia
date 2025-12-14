from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('alumno/<str:codigo_usuario>/datos/', AlumnoDatosView.as_view(), name='alumno-datos'),
    path('alumno/<str:codigo_usuario>/cursos/', AlumnoCursosView.as_view(), name='alumno-cursos'),
    path('alumno/<str:codigo_usuario>/ciclo/<str:id_ciclo>/notas/', AlumnoNotasView.as_view(), name='alumno-notas'),
    path('alumno/<str:codigo_usuario>/proximo-simulacro/', AlumnoProximoSimulacroView.as_view(), name='alumno-proximo-simulacro'),
    path('alumno/<str:codigo_usuario>/asistencia/', AlumnoAsistenciaView.as_view(), name='alumno-asistencia'),
    path('docente/<str:codigo_usuario>/datos/', DocenteDatosView.as_view(), name='docente-datos'),
    path('docente/<str:codigo_usuario>/cursos/', DocenteCursosView.as_view(), name='docente-cursos'),
    path('tutor/<str:codigo_usuario>/datos/', TutorDatosView.as_view(), name='tutor-datos'),
    path('tutor/<str:codigo_usuario>/ciclos/', TutorCiclosView.as_view(), name='tutor-ciclos'),
    path('tutor/<str:codigo_usuario>/ciclo/<str:id_ciclo>/simulacros/', TutorCicloSimulacrosView.as_view(), name='tutor-ciclo-simulacros'),
    path('tutor/<str:codigo_usuario>/ciclo/<str:id_ciclo>/alumnos/', TutorCicloAlumnosView.as_view(), name='tutor-ciclo-alumnos')
]
