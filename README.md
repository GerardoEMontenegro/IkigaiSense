# URL DESPLEGADA
[miblog.pythonanywhere.com](https://ikigaicenter.pythonanywhere.com/)

## Descripción

IkigaiSense es una plataforma desarrollada con Python y Django que permite la gestión de publicaciones, comentarios y usuarios, orientada a la comunidad interesada en el desarrollo personal y profesional, en el ambito deportivo.

---

## Características

- Registro y autenticación de usuarios (colaboradores y administradores)
- Creación, edición y eliminación de publicaciones
- Sistema de comentarios en los posts
- Gestión de categorías
- Recuperación de contraseña
- Panel de administración personalizado
- Carga de imágenes para posts y perfiles de usuario

---

# Integrantes

- Cintia
- German
- Gerardo

# USUARIOS DE PRUEBA

COLABORADOR  
email: CintiRomi  
contraseña: facil123

COLABORADOR  
Usuario: gd_25  
contraseña: German.25

ADMIN  
Usuario: gerardo1  
contraseña: casa.2020

## DEJAMOS 10 Post de prueba

# Proyecto creado con Python y Django

# Estructura del proyecto (incluyendo archivos principales de entorno, apps y templates):

```
IkigaiSense/
├── entorno/                           # Carpeta del entorno virtual
│   ├── Include/
│   ├── Lib/
│   ├── Scripts/
│   │   ├── activate
│   │   ├── activate.bat
│   │   ├── deactivate.bat
│   │   ├── pip.exe
│   │   ├── python.exe
│   │   └── ...
│   ├── pyvenv.cfg
│   └── ...
├── apps/
│   ├── categories/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── comments/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── post/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   └── user/
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── migrations/
│       │   └── __init__.py
│       ├── models.py
│       ├── templatetags/
│       │   └── __init__.py
│       ├── tests.py
│       ├── urls.py
│       └── views.py
├── blog/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── media/
│   ├── post/cover/
│   └── user/
├── static/
│   ├── assets/
│   └── js/
├── templates/
│   ├── auth/
│   │   ├── login.html
│   │   ├── logout.html
│   │   ├── register.html
│   │   ├── password_change.html
│   │   ├── password_change_done.html
│   │   └── ...
│   ├── category/
│   │   ├── category_list.html
│   │   ├── category_detail.html
│   │   ├── category_form.html
│   │   └── ...
│   ├── components/
│   │   ├── navbar.html
│   │   ├── footer.html
│   │   └── ...
│   ├── layouts/
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── sidebar.html
│   │   └── ...
│   ├── post/
│   │   ├── post_list.html
│   │   ├── post_detail.html
│   │   ├── post_form.html
│   │   └── ...
│   ├── ps_reset/
│   │   ├── password_reset_form.html
│   │   ├── password_reset_done.html
│   │   ├── password_reset_confirm.html
│   │   └── password_reset_complete.html
│   ├── user/
│   │   ├── profile.html
│   │   ├── update.html
│   │   └── ...
│   ├── index.html
│   └── about.html
├── manage.py
└── requirements.txt