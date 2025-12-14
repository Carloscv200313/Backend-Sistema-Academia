from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from django.db import connection
from django.utils import timezone


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        role = request.data.get('role')

        try:
            usuario = Usuario.objects.get(codigo_usuario=username, contrasena_usuario=password, rol=role)
            if role == 'alumno':
                alumno = Alumno.objects.get(id_usuario=usuario)
                user_data = {
                    'id': alumno.id_alumno,
                    'nombre': alumno.nombre_alumno,
                    'role': usuario.rol
                }
            elif role == 'docente':
                docente = Docente.objects.get(id_usuario=usuario)
                user_data = {
                    'id': docente.id_docente,
                    'nombre': docente.nombre_docente,
                    'role': usuario.rol
                }
            elif role == 'tutor':
                tutor = Tutor.objects.get(id_usuario=usuario)
                user_data = {
                    'id': tutor.id_tutor,
                    'nombre': tutor.nombre_tutor,
                    'role': usuario.rol
                }
            else:
                return Response({'error': 'Rol no válido'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'token': 'abcdef123...',  # Placeholder
                'user': user_data
            }, status=status.HTTP_200_OK)

        except Usuario.DoesNotExist:
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
        except (Alumno.DoesNotExist, Docente.DoesNotExist, Tutor.DoesNotExist):
            return Response({'error': 'Usuario no encontrado para el rol especificado'}, status=status.HTTP_404_NOT_FOUND)

class AlumnoDatosView(APIView):
    def get(self, request, codigo_usuario):
        try:
            alumno = Alumno.objects.get(id_alumno=codigo_usuario)
            serializer = AlumnoSerializer(alumno)
            return Response(serializer.data)
        except (Alumno.DoesNotExist, Usuario.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

class AlumnoCursosView(APIView):
    def get(self, request, codigo_usuario):
        try:
            # Primero obtenemos el alumno
            alumno = Alumno.objects.get(id_alumno=codigo_usuario)
            print(f"Alumno encontrado: {alumno.id_alumno}")
            # Usamos SQL directo para evitar problemas con PK compuestas
            with connection.cursor() as cursor:
                # Consulta equivalente a lo que intentabas hacer
                cursor.execute("""
                    SELECT 
                        c.id_curso,
                        c.nombre_curso,
                        cc.id_docente,
                        d.nombre_docente,
                        hc.dia_semana,
                        hc.hora_inicio,
                        hc.hora_fin,
                        ci.nombre_ciclo
                    FROM alumno_ciclo_curso acc
                    INNER JOIN curso c ON acc.id_curso = c.id_curso
                    INNER JOIN ciclo ci ON acc.id_ciclo = ci.id_ciclo
                    LEFT JOIN ciclo_curso cc ON 
                        cc.id_ciclo = acc.id_ciclo 
                        AND cc.id_curso = acc.id_curso
                    LEFT JOIN docente d ON cc.id_docente = d.id_docente
                    LEFT JOIN horario_curso hc ON 
                        hc.id_ciclo = acc.id_ciclo 
                        AND hc.id_curso = acc.id_curso
                    WHERE acc.id_alumno = %s
                    ORDER BY c.nombre_curso, hc.dia_semana
                """, [alumno.id_alumno])
                # Procesamos los resultados
                columns = [col[0] for col in cursor.description]
                resultados = cursor.fetchall()
                
                cursos = []
                for row in resultados:
                    row_dict = dict(zip(columns, row))
                    cursos.append({
                        'id': row_dict['id_curso'],
                        'nombre': row_dict['nombre_curso'],
                        'ciclo': row_dict['nombre_ciclo'],
                        'dias': row_dict['dia_semana'],
                        'hora': f"{row_dict['hora_inicio']} - {row_dict['hora_fin']}" if row_dict['hora_inicio'] and row_dict['hora_fin'] else None,
                        'docente': row_dict['nombre_docente'],
                        'id_docente': row_dict['id_docente']
                    })
            
            return Response(cursos)
            
        except Alumno.DoesNotExist:
            return Response(
                {'error': 'Alumno no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"Error: {e}")
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class AlumnoNotasView(APIView):
    def get(self, request, codigo_usuario, id_ciclo):
        try:
            alumno = Alumno.objects.get(id_alumno=codigo_usuario)
            print(f"Alumno encontrado: {alumno.id_alumno}")
            simulacros_alumno = SimulacroAlumno.objects.filter(id_alumno=alumno)
            print(f"Simulacros del alumno: {simulacros_alumno}")
            notas = []
            for sa in simulacros_alumno:
                simulacro = sa.id_simulacro
                notas.append({
                    'id': simulacro.id_simulacro,
                    'nombre': simulacro.nombre_simulacro,
                    'semana': 1,  # Placeholder
                    'dia': simulacro.fecha,
                    'nota': sa.nota
                })
            return Response(notas)
        except (Alumno.DoesNotExist, Usuario.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

class AlumnoProximoSimulacroView(APIView):
    def get(self, request, codigo_usuario):
        try:
            alumno = Alumno.objects.get(id_alumno=codigo_usuario)
            print(f"Alumno encontrado: {alumno.id_alumno}")
            hoy = timezone.now().date()
            
            # Buscar el próximo simulacro no tomado
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        s.id_simulacro,
                        s.nombre_simulacro,
                        s.fecha,
                        (s.fecha - %s) as dias_restantes
                    FROM simulacro s
                    WHERE s.fecha >= %s
                        AND s.id_simulacro NOT IN (
                            SELECT id_simulacro 
                            FROM simulacro_alumno 
                            WHERE id_alumno = %s
                        )
                    ORDER BY s.fecha ASC
                    LIMIT 1
                """, [hoy, hoy, alumno.id_alumno])
                
                proximo_simulacro = cursor.fetchone()
                
                if proximo_simulacro:
                    id_simulacro, nombre, fecha, dias_restantes = proximo_simulacro
                    
                    # Determinar proximidad
                    if dias_restantes == 0:
                        proximidad = "HOY"
                        mensaje = "¡Hoy es el día del simulacro!"
                    elif dias_restantes == 1:
                        proximidad = "MAÑANA"
                        mensaje = "¡Mañana es el simulacro!"
                    elif dias_restantes <= 7:
                        proximidad = "ESTA SEMANA"
                        mensaje = f"El simulacro es esta semana ({dias_restantes} días)"
                    elif dias_restantes <= 14:
                        proximidad = "PRÓXIMA SEMANA"
                        mensaje = f"El simulacro es la próxima semana"
                    else:
                        proximidad = "PRÓXIMAMENTE"
                        mensaje = f"El simulacro es en {dias_restantes} días"
                    
                    return Response({
                        "id": id_simulacro,
                        "nombre": nombre,
                        "fecha": fecha.strftime('%Y-%m-%d'),
                        "fecha_formateada": fecha.strftime('%d %b, %Y'),
                        "dia_semana": fecha.strftime('%A'),
                        "dias_restantes": dias_restantes,
                        "proximidad": proximidad,
                        "mensaje": mensaje,
                        "ya_tomado": False
                    })
                else:
                    # Si no hay próximos, buscar el último completado
                    cursor.execute("""
                        SELECT 
                            s.id_simulacro,
                            s.nombre_simulacro,
                            s.fecha,
                            sa.nota
                        FROM simulacro_alumno sa
                        INNER JOIN simulacro s ON sa.id_simulacro = s.id_simulacro
                        WHERE sa.id_alumno = %s
                        ORDER BY s.fecha DESC
                        LIMIT 1
                    """, [alumno.id_alumno])
                    
                    ultimo_simulacro = cursor.fetchone()
                    
                    if ultimo_simulacro:
                        id_simulacro, nombre, fecha, nota = ultimo_simulacro
                        return Response({
                            "id": id_simulacro,
                            "nombre": nombre,
                            "fecha": fecha.strftime('%Y-%m-%d'),
                            "fecha_formateada": fecha.strftime('%d %b, %Y'),
                            "dia_semana": fecha.strftime('%A'),
                            "dias_restantes": 0,
                            "proximidad": "COMPLETADO",
                            "mensaje": f"Último simulacro completado con nota: {nota}",
                            "nota": nota,
                            "ya_tomado": True
                        })
                    else:
                        return Response({
                            "mensaje": "No tienes simulacros programados",
                            "proximidad": "SIN SIMULACROS"
                        })
                        
        except Alumno.DoesNotExist:
            return Response(
                {'error': 'Alumno no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )

class AlumnoAsistenciaView(APIView):
    def get(self, request, codigo_usuario):
        # Placeholder logic
        return Response({"porcentaje": 100})

class DocenteDatosView(APIView):
    def get(self, request, codigo_usuario):
        try:
            docente = Docente.objects.get(id_docente=codigo_usuario)
            serializer = DocenteSerializer(docente)
            return Response(serializer.data)
        except (Docente.DoesNotExist, Usuario.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)



class DocenteCursosView(APIView):
    def get(self, request, codigo_usuario):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    cc.id_curso,
                    c.nombre_curso,
                    h.dia_semana,
                    h.hora_inicio,
                    h.hora_fin,
                    COUNT(acc.id_alumno) AS alumnos
                FROM ciclo_curso cc
                INNER JOIN curso c
                    ON c.id_curso = cc.id_curso
                LEFT JOIN horario_curso h
                    ON h.id_ciclo = cc.id_ciclo
                   AND h.id_curso = cc.id_curso
                LEFT JOIN alumno_ciclo_curso acc
                    ON acc.id_ciclo = cc.id_ciclo
                   AND acc.id_curso = cc.id_curso
                WHERE cc.id_docente = %s
                GROUP BY
                    cc.id_curso,
                    c.nombre_curso,
                    h.dia_semana,
                    h.hora_inicio,
                    h.hora_fin
                ORDER BY
                    c.nombre_curso,
                    h.dia_semana,
                    h.hora_inicio
            """, [codigo_usuario])

            rows = cursor.fetchall()

        # Si no hay cursos/horarios para ese docente
        if not rows:
            return Response([], status=status.HTTP_200_OK)

        cursos = []
        for row in rows:
            (
                id_curso,
                nombre_curso,
                dia_semana,
                hora_inicio,
                hora_fin,
                alumnos_count,
            ) = row

            cursos.append({
                "id": id_curso,
                "nombre": nombre_curso,
                "dias": dia_semana,
                "hora": f"{hora_inicio} - {hora_fin}" if hora_inicio and hora_fin else None,
                "alumnos": alumnos_count,
            })

        return Response(cursos, status=status.HTTP_200_OK)




class TutorDatosView(APIView):
    def get(self, request, codigo_usuario):
        try:
            tutor = Tutor.objects.get(id_tutor=codigo_usuario)
            serializer = TutorSerializer(tutor)
            return Response(serializer.data)
        except (Tutor.DoesNotExist, Usuario.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

class TutorCiclosView(APIView):
    def get(self, request, codigo_usuario):
        try:
            ciclos = Ciclo.objects.filter(id_tutor=codigo_usuario)
            print(ciclos)
            ciclos_data = []
            for ciclo in ciclos:
                alumnos_count = Alumno.objects.filter(id_tutor=codigo_usuario).count()
                ciclos_data.append({
                    'id': ciclo.id_ciclo,
                    'nombre': ciclo.nombre_ciclo,
                    'alumnos': alumnos_count
                })
            return Response(ciclos_data)
        except (Tutor.DoesNotExist, Usuario.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

class TutorCicloSimulacrosView(APIView):
    def get(self, request, codigo_usuario, id_ciclo):
        # Placeholder logic
        return Response([
            {
                "id": 7,
                "nombre": "General",
                "dia": "Jul 20, 2024",
            }
        ])


class TutorCicloAlumnosView(APIView):
    def get(self, request, codigo_usuario, id_ciclo):
        """
        Obtiene alumnos con los cursos que llevan en el ciclo
        """
        try:
            with connection.cursor() as cursor:
                # Primero obtenemos todos los alumnos del ciclo
                cursor.execute("""
                    SELECT DISTINCT
                        a.id_alumno,
                        a.nombre_alumno,
                        u.codigo_usuario
                    FROM alumno a
                    INNER JOIN alumno_ciclo_curso acc 
                        ON a.id_alumno = acc.id_alumno
                    INNER JOIN usuario u 
                        ON a.id_usuario = u.id_usuario
                    WHERE acc.id_ciclo = %s
                    ORDER BY a.nombre_alumno
                """, [id_ciclo])
                
                alumnos_basicos = cursor.fetchall()
                
                # Para cada alumno, obtenemos sus cursos en este ciclo
                alumnos_completos = []
                for id_alumno, nombre, codigo in alumnos_basicos:
                    cursor.execute("""
                        SELECT 
                            c.id_curso,
                            c.nombre_curso,
                            c.horas_de_clase,
                            d.nombre_docente,
                            h.dia_semana,
                            h.hora_inicio,
                            h.hora_fin
                        FROM alumno_ciclo_curso acc
                        INNER JOIN curso c 
                            ON acc.id_curso = c.id_curso
                        LEFT JOIN ciclo_curso cc 
                            ON cc.id_ciclo = acc.id_ciclo 
                            AND cc.id_curso = acc.id_curso
                        LEFT JOIN docente d 
                            ON cc.id_docente = d.id_docente
                        LEFT JOIN horario_curso h 
                            ON h.id_ciclo = acc.id_ciclo 
                            AND h.id_curso = acc.id_curso
                        WHERE acc.id_alumno = %s 
                            AND acc.id_ciclo = %s
                        ORDER BY c.nombre_curso
                    """, [id_alumno, id_ciclo])
                    
                    cursos = cursor.fetchall()
                    cursos_list = [
                        {
                            'id_curso': curso[0],
                            'nombre_curso': curso[1],
                            'horas_clase': curso[2],
                            'docente': curso[3],
                            'dia_semana': curso[4],
                            'horario': f"{curso[5]} - {curso[6]}" if curso[5] and curso[6] else None
                        }
                        for curso in cursos
                    ]
                    
                    alumnos_completos.append({
                        'id_alumno': id_alumno,
                        'nombre_alumno': nombre,
                        'codigo_usuario': codigo,
                        'total_cursos': len(cursos_list),
                        'cursos': cursos_list
                    })
            
            return Response({
                'ciclo_id': id_ciclo,
                'total_alumnos': len(alumnos_completos),
                'alumnos': alumnos_completos
            })
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class TutorCicloAlumnoInfoView(APIView):
    def get(self, request, codigo_usuario, id_ciclo, id_alumno):
        try:
            tutor = Tutor.objects.get(id_usuario__codigo_usuario=codigo_usuario)
            alumno = Alumno.objects.get(id_alumno=id_alumno, id_tutor=tutor, id_ciclo=id_ciclo)
            serializer = AlumnoSerializer(alumno)
            return Response(serializer.data)
        except (Tutor.DoesNotExist, Usuario.DoesNotExist, Alumno.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

class TutorCicloAsistenciaView(APIView):
    def put(self, request, codigo_usuario, id_ciclo):
        asistencias = request.data
        for asistencia_data in asistencias:
            Asistencia.objects.update_or_create(
                id_alumno_id=asistencia_data['id'],
                id_ciclo_id=id_ciclo,
                fecha=date.today(), # Placeholder
                defaults={'estado_asistencia': asistencia_data['estado']}
            )
        return Response(status=status.HTTP_200_OK)

class TutorSimulacroNotasView(APIView):
    def put(self, request, codigo_usuario, id_ciclo, id_simulacro):
        notas = request.data
        for nota_data in notas:
            SimulacroAlumno.objects.update_or_create(
                id_alumno_id=nota_data['id'],
                id_simulacro_id=id_simulacro,
                defaults={'nota': nota_data['nota']}
            )
        return Response(status=status.HTTP_200_OK)
