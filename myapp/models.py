from django.db import models

class Usuario(models.Model):
    id_usuario = models.CharField(primary_key=True, max_length=255)
    codigo_usuario = models.CharField(max_length=50, unique=True)
    contrasena_usuario = models.CharField(max_length=150)
    rol = models.CharField(max_length=20)

    @property
    def pk(self):
        return self.id_usuario

    class Meta:
        db_table = 'usuario'

class Apoderado(models.Model):
    id_apoderado = models.CharField(primary_key=True)
    nombre_apoderado = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=9, blank=True, null=True)
    parentesco = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'apoderado'

class Tutor(models.Model):
    id_tutor = models.CharField(primary_key=True)
    nombre_tutor = models.CharField(max_length=100, blank=True, null=True)
    dni = models.CharField(max_length=8, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    telefono = models.CharField(max_length=9, blank=True, null=True)
    correo_electronico = models.CharField(max_length=100, blank=True, null=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario', blank=True, null=True)

    class Meta:
        db_table = 'tutor'

class Alumno(models.Model):
    id_alumno = models.CharField(primary_key=True)
    nombre_alumno = models.CharField(max_length=100, blank=True, null=True)
    dni = models.CharField(max_length=8, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    telefono = models.CharField(max_length=9, blank=True, null=True)
    direccion = models.CharField(max_length=150, blank=True, null=True)
    correo_electronico = models.CharField(max_length=100, blank=True, null=True)
    nivel_educativo = models.CharField(max_length=50, blank=True, null=True)
    id_apoderado = models.ForeignKey(Apoderado, on_delete=models.CASCADE, db_column='id_apoderado')
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    id_tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, db_column='id_tutor')

    class Meta:
        db_table = 'alumno'

class Docente(models.Model):
    id_docente = models.CharField(primary_key=True)
    nombre_docente = models.CharField(max_length=100, blank=True, null=True)
    dni = models.CharField(max_length=8, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    telefono = models.CharField(max_length=9, blank=True, null=True)
    correo_electronico = models.CharField(max_length=100, blank=True, null=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario', blank=True, null=True)

    class Meta:
        db_table = 'docente'

class Ciclo(models.Model):
    id_ciclo = models.CharField(primary_key=True)
    nombre_ciclo = models.CharField(max_length=50, blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    id_tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, db_column='id_tutor', blank=True, null=True)
    class Meta:
        db_table = 'ciclo'

class Curso(models.Model):
    id_curso = models.CharField(primary_key=True)
    nombre_curso = models.CharField(max_length=100, blank=True, null=True)
    horas_de_clase = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'curso'

class CicloCurso(models.Model):
    id_ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE, db_column='id_ciclo')
    id_curso = models.ForeignKey(Curso, on_delete=models.CASCADE, db_column='id_curso')
    id_docente = models.ForeignKey(Docente, on_delete=models.CASCADE, db_column='id_docente', blank=True, null=True)

    class Meta:
        db_table = 'ciclo_curso'
        unique_together = (('id_ciclo', 'id_curso'),)

class AlumnoCicloCurso(models.Model):
    id_alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, db_column='id_alumno')
    id_ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE, db_column='id_ciclo')
    id_curso = models.ForeignKey(Curso, on_delete=models.CASCADE, db_column='id_curso')

    class Meta:
        db_table = 'alumno_ciclo_curso'
        unique_together = (('id_alumno', 'id_ciclo', 'id_curso'),)

class Simulacro(models.Model):
    id_simulacro = models.CharField(primary_key=True)
    nombre_simulacro = models.CharField(max_length=100, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'simulacro'

class SimulacroAlumno(models.Model):
    id_simulacro = models.ForeignKey(
        Simulacro,
        on_delete=models.CASCADE,
        db_column='id_simulacro',
        primary_key=True,  # 👈 Django dejará de buscar "id"
    )
    id_alumno = models.ForeignKey(
        Alumno,
        on_delete=models.CASCADE,
        db_column='id_alumno'
    )
    nota = models.DecimalField(
        max_digits=5,     # Ej: 20.00 -> 5 dígitos en total
        decimal_places=2, # 2 decimales
        null=True,
        blank=True,
    )
    class Meta:
        db_table = 'simulacro_alumno'
        managed = False  # 👈 importante si la tabla ya existe
        unique_together = (('id_simulacro', 'id_alumno'),)


class HorarioCurso(models.Model):
    id_horario = models.AutoField(primary_key=True)
    id_ciclo_curso = models.ForeignKey(CicloCurso, on_delete=models.CASCADE, db_column='id_ciclo_curso')
    dia_semana = models.CharField(max_length=15, blank=True, null=True)
    hora_inicio = models.TimeField(blank=True, null=True)
    hora_fin = models.TimeField(blank=True, null=True)

    class Meta:
        db_table = 'horario_curso'

class Asistencia(models.Model):
    id_asistencia = models.AutoField(primary_key=True)
    id_alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, db_column='id_alumno')
    id_ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE, db_column='id_ciclo')
    fecha = models.DateField()
    estado_asistencia = models.CharField(max_length=10)

    class Meta:
        db_table = 'asistencia'
        unique_together = (('id_alumno', 'id_ciclo', 'fecha'),)