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
.
├── .env
├── .gitignore
├── README.md
├── requirements.txt
└── blog/
    ├── manage.py
    ├── apps/
    │   ├── categorias/
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── models.py
    │   │   ├── tests.py
    │   │   ├── views.py
    │   │   └── migrations/
    │   │       └── __init__.py
    │   ├── comments/
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── forms.py
    │   │   ├── models.py
    │   │   ├── tests.py
    │   │   ├── urls.py
    │   │   ├── views.py
    │   │   └── migrations/
    │   │       └── __init__.py
    │   ├── post/
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── forms.py
    │   │   ├── models.py
    │   │   ├── tests.py
    │   │   ├── urls.py
    │   │   ├── views.py
    │   │   └── migrations/
    │   │       ├── 0001_initial.py
    │   │       ├── 0002_initial.py
    │   │       ├── 0003_rating.py
    │   │       ├── ...
    │   │       └── __init__.py
    │   └── user/
    │       ├── admin.py
    │       ├── apps.py
    │       ├── forms.py
    │       ├── models.py
    │       ├── signals.py
    │       ├── tests.py
    │       ├── urls.py
    │       ├── views.py
    │       ├── templatetags/
    │       │   ├── user_groups.py
    │       │   └── __init__.py
    │       └── migrations/
    │           ├── 0001_initial.py
    │           ├── 0002_alter_user_alias_alter_user_avatar_alter_user_email.py
    │           ├── 0003_alter_user_avatar.py
    │           └── __init__.py
    ├── blog/
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   ├── views.py
    │   ├── wsgi.py
    │   └── configurations/
    │       ├── base.py
    │       ├── local.py
    │       └── production.py
    ├── static/
    │   ├── assets/
    │   │   ├── colesterol.png
    │   │   ├── default-avatar.png
    │   │   ├── favicon2.png
    │   │   ├── login-side-image.jpeg
    │   │   ├── logo.png
    │   │   └── logo2.png
    │   ├── images/
    │   │   ├── 500_333.png
    │   │   ├── 805929522_237198349_1024x576.webp
    │   │   ├── Alegría.jpg
    │   │   ├── portada1.avif
    │   │   └── ...
    │   ├── svg/
    │   │   ├── facebook.svg
    │   │   ├── instagram.svg
    │   │   └── pinterest.svg
    │   └── js/
    │       └── tailwind.js
    ├── templates/
    │   ├── layouts/
    │   │   ├── auth_layout.html
    │   │   ├── base_layout.html
    │   │   ├── general_layout.html
    │   │   └── post_layout.html
    │   ├── components/
    │   │   ├── commons/
    │   │   │   ├── footer.html
    │   │   │   └── heather.html
    │   │   └── ui/
    │   │       └── navbar.html
    │   ├── post/
    │   │   ├── comment_confirm_delete.html
    │   │   ├── post_confirm_delete.html
    │   │   ├── post_create.html
    │   │   ├── post_detail.html
    │   │   ├── post_list.html
    │   │   ├── post_scripts.html
    │   │   └── post_update.html
    │   ├── user/
    │   │   ├── update_avatar.html
    │   │   └── user_profile.html
    │   ├── auth/
    │   │   ├── auth_login.html
    │   │   ├── auth_register.html
    │   │   ├── password_reset.html
    │   │   ├── password_reset_complete.html
    │   │   ├── password_reset_confirm.html
    │   │   └── password_reset_done.html
    │   └── category/
    │       ├── category_create.html
    │       └── category_detail.html
    └── media/
        ├── post/
        │   └── cover/
        │       ├── post_09cc903a-2d3d-4aab-9ce0-beeda1ef3548_img_8f922df1.png
        │       ├── post_157fe85d-50d3-4dd9-aa1d-7526413eca15_img_893a0632.jpeg
        │       └── ...
        └── user/
            ├── avastar/
            │   ├── user_1654809b-d335-4fa5-965f-70efc546f642_avatar.jpg
            │   └── ...
            └── default/
                └── default-avatar.png

---

## 📝 Licencia

Este proyecto está bajo la licencia **MIT**.  
Puedes consultar el archivo completo de licencia [aquí](LICENSE).

MIT License

Copyright (c) 2025 Gerardo Montenegro, Cintia Romina Bertoncini, German Edgardo Delfino

Se concede permiso, de forma gratuita, a cualquier persona que obtenga una copia
de este software y los archivos de documentación asociados (el "Software"), para
tratar en el Software sin restricción, incluyendo sin limitación los derechos
de usar, copiar, modificar, fusionar, publicar, distribuir, sublicenciar y/o
vender copias del Software, y permitir a las personas a quienes se les proporcione
el Software que lo hagan, sujeto a las siguientes condiciones:

El aviso de copyright y este aviso de permiso se incluirán en todas las copias
o partes sustanciales del Software.

EL SOFTWARE SE PROPORCIONA "TAL CUAL", SIN GARANTÍA DE NINGÚN TIPO, EXPRESA O
IMPLÍCITA, INCLUYENDO PERO NO LIMITADO A LAS GARANTÍAS DE COMERCIALIZACIÓN,
IDONEIDAD PARA UN PROPÓSITO PARTICULAR Y NO INFRACCIÓN. EN NINGÚN CASO LOS
AUTORES O TITULARES DE LOS DERECHOS DE AUTOR SERÁN RESPONSABLES DE NINGUNA
RECLAMACIÓN, DAÑO O OTRA RESPONSABILIDAD, YA SEA EN UNA ACCIÓN DE CONTRATO,
AGRAVIO O DE OTRA FORMA, DERIVADA DEL SOFTWARE O DEL USO U OTRO TIPO DE
OPERACIONES EN EL SOFTWARE.
