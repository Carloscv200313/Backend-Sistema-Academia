
# Proyecto Academia

Este es el backend de un sistema de gestión académica, diseñado para facilitar la interacción entre alumnos, docentes y tutores. La API RESTful proporciona endpoints para gestionar datos de usuarios, cursos, notas, asistencia y más.

## Características

- **Gestión de usuarios:** Sistema de roles para Alumnos, Docentes y Tutores con autenticación.
- **Consultas académicas:** Permite a los alumnos ver sus cursos, notas, horarios y asistencia.
- **Gestión de cursos:** Los docentes pueden ver los cursos que imparten y la cantidad de alumnos.
- **Tutoría:** Los tutores pueden hacer seguimiento de los ciclos, alumnos a su cargo, y el rendimiento en los simulacros.

## Tecnologías Utilizadas

- **Backend:** Python, Django, Django REST Framework
- **Base de datos:** SQLite (por defecto en desarrollo)
- **Autenticación:** Basada en Tokens

## Instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone https://URL_DEL_REPOSITORIO/Max-Hule.git
    cd Max-Hule
    ```

2.  **Crear y activar un entorno virtual:**
    ```bash
    python -m venv venv
    # En Windows
    venv\Scripts\activate
    # En macOS/Linux
    source venv/bin/activate
    ```

3.  **Instalar dependencias:**
    Asegúrate de tener un archivo `requirements.txt`. Si no, puedes crearlo a partir de las librerías que estás usando.
    ```bash
    pip install -r requirements.txt
    ```
    Si no tienes un `requirements.txt`, instala Django y Django REST Framework:
    ```bash
    pip install django djangorestframework
    ```

4.  **Realizar las migraciones:**
    ```bash
    python manage.py migrate
    ```

## Uso

1.  **Iniciar el servidor de desarrollo:**
    ```bash
    python manage.py runserver
    ```
    El servidor estará disponible en `http://127.0.0.1:8000/`.

2.  **Crear un superusuario (opcional):**
    Para acceder al panel de administración de Django.
    ```bash
    python manage.py createsuperuser
    ```

## API Endpoints

La API proporciona varios endpoints para interactuar con el sistema. La autenticación es requerida para la mayoría de las rutas.

- **Autenticación:** `POST /api/login/`
- **Endpoints de Alumno:** `/api/alumno/...`
- **Endpoints de Docente:** `/api/docente/...`
- **Endpoints de Tutor:** `/api/tutor/...`

Para una descripción detallada de todos los endpoints, consulta el archivo `endpoints_documentacion.txt`.

## Esquema de la Base de Datos

El diseño de la base de datos incluye tablas para usuarios, alumnos, docentes, tutores, cursos, ciclos, simulacros y más.

Para ver el esquema completo en formato SQL, consulta el archivo `schema-database.txt`.

## Contribuir

Las contribuciones son bienvenidas. Para contribuir, por favor, haz un fork del repositorio, crea una nueva rama, realiza tus cambios y abre un Pull Request.
