# Artistry API — Backend FastAPI

Backend REST para la plataforma profesional de maquillaje Artistry by Sara MUA, desarrollado con FastAPI + SQLAlchemy + PostgreSQL, con autenticación JWT y control de acceso por roles. Permite gestionar servicios de maquillaje, reservas, clases online y tres tipos de usuarios: visitantes, usuarios registrados y administrador.

# Tecnologías utilizadas

- Python 3

- FastAPI

- SQLAlchemy ORM

- PostgreSQL

- Alembic (migraciones)

- JWT (python-jose)

- Passlib (hash de contraseñas)

- Uvicorn (servidor)

- Pydantic (validación)

# Instalación y ejecución

1.  Clonar repositorio:

        git clone https://github.com/monicahdev/artistry_api.git

2.  Crear entorno virtual:

        python -m venv .venv
        source .venv/Scripts/activate - Windows

3.  Instalar dependencias:

        pip install -r requirements.txt

4.  Configurar variables de entorno .env:

        Ejemplo:

        DATABASE_URL=postgresql://user:password@localhost/artistry
        SECRET_KEY=password
        ALGORITHM=HS256
        ACCESS_TOKEN_EXPIRE_MINUTES=60

5.  Ejecutar servidor:

          uvicorn app.main:app --reload

# API disponible en:

    http://127.0.0.1:8000

# Swagger interactivo para probar endpoints:

    http://127.0.0.1:8000/docs

# Autora

- Artistry by Sara MUA — backend desarrollado como parte del Trabajo Final de Máster en Desarrollo de Sitios y Aplicaciones Web de la Universitat Oberta de Catalunya (UOC) por **Mónica Natalia Hernández Barrera**

# Licencia

POR CONFIRMAR
