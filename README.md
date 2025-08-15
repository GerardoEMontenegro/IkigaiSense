<p align="center">
  <img src="https://raw.githubusercontent.com/GerardoEMontenegro/IkigaiSense/refs/heads/main/blog/static/assets/logo2.png" alt="Ikigai Center Logo" width="150"/>
</p>

<h1 align="center">🌿 Ikigai Center</h1>
<p align="center">
  Plataforma de blog enfocada en <strong>salud, bienestar y crecimiento personal</strong>, desarrollada en <strong>Django</strong> con un diseño moderno y minimalista.
</p>

<p align="center">
  <a href="https://ikigaicenter.pythonanywhere.com/">🔗 Visitar el proyecto</a> | 
  <a href="#🚀-características">✨ Características</a> | 
  <a href="#🛠️-tecnologías-utilizadas">🛠️ Tecnologías</a> | 
  <a href="#📂-estructura-del-proyecto">📂 Estructura</a>
</p>

---

## 🚀 Características

- 📚 Publicación y gestión de artículos por categorías  
- 🖼️ Imágenes destacadas y galería para cada post  
- 💬 Sistema de comentarios y reacciones con emojis  
- 🔒 Registro e inicio de sesión con email o redes sociales  
- 🌐 Diseño responsive y multilenguaje  
- ⭐ Favoritos y lista de lectura pendiente  

---

## 🛠️ Tecnologías utilizadas

<p align="center">
  <img src="https://img.shields.io/badge/Django-5.0-green" alt="Django">
  <img src="https://img.shields.io/badge/Python-3.11-blue" alt="Python">
  <img src="https://img.shields.io/badge/TailwindCSS-3.5-teal" alt="TailwindCSS">
  <img src="https://img.shields.io/badge/Alpine.js-3.12-purple" alt="Alpine.js">
</p>

- **Backend:** Django 5, Python 3  
- **Frontend:** HTML5, TailwindCSS, Alpine.js  
- **Base de datos:** SQLite (desarrollo) / PostgreSQL (producción)  
- **Autenticación:** Django Allauth  
- **Otros:** Pillow, Crispy Forms, Widget Tweaks  

---

## 👥 Integrantes

- Cintia Romina Bertoncini  
- German Edgardo Delfino  
- Gerardo Emanuel Montenegro  

---

## 🔑 Usuarios de prueba

**COLABORADOR**  
- Usuario: `CintiRomi`  
- Contraseña: `facil123`  

**COLABORADOR**  
- Usuario: `gd_25`  
- Contraseña: `German.25`  

**ADMIN**  
- Usuario: `gerardo1`  
- Contraseña: `casa.2020`  

> 💡 Se han cargado **10 posts de prueba**.

---

## 🖼️ Captura de pantalla

<p align="center">
  <img src="https://raw.githubusercontent.com/usuario/ikigai-center/main/static/assets/screenshot_home.png" alt="Ikigai Center Home" width="700"/>
</p>

---

## 📂 Estructura del proyecto

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
