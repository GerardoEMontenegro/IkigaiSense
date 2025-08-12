from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from django.contrib.auth.models import Group  
from apps.user.models import User


class CustomUserAdmin(admin.ModelAdmin):  # Clase personalizada para el administrador de usuarios
    fieldsets = UserAdmin.fieldsets + (  # Agrega los campos personalizados al administrador de usuarios
        (None, {'fields': ('alias', 'avatar')}),  # Campos personalizados: alias y avatar
    )

    add_fieldsets = (  # Agrega los campos personalizados al formulario de creación de usuarios
        (None, {
            'fields': ('username', 'email', 'alias', 'avatar', 'password1', 'password2')
            }),
    )

    def is_registered(self, obj):   # Verifica si el usuario pertenece al grupo 'registered'
        return obj.groups.filter(name= 'registered').exists()  # Verifica si el usuario pertenece al grupo 'registered'
    is_registered.short_description = 'Es usuario registrado'  # Descripción del campo en el administrador
    is_registered.boolean = True  # Muestra un icono en lugar de texto

    def is_colaborator(self, obj):
        return obj.groups.filter(name='Colaborator').exists()
    is_colaborator.short_description = 'Es colaborador'  # Descripción del campo en el administrador
    is_colaborator.boolean = True  # Muestra un icono en lugar de texto

    def is_admin(self, obj):
        return obj.groups.filter(name='Admin').exists()
    is_admin.short_description = 'Es administrador'  # Descripción del campo en el administrador
    is_admin.boolean = True  # Muestra un icono en lugar de texto

#/DEFINIENDO LAS ACCIONES PERSONALIZADAS PARA EL ADMINISTRADOR DE USUARIOS/

    def add_to_registered(self, request, queryset):
        registered_group = Group.objects.get_or_create (name='Registered')  # Obtiene el grupo 'Registered'
        for user in queryset:
            user.groups.add(registered_group)
        self.message_user(request, "Usuarios añadidos al grupo 'Registered'")  # Mensaje de éxito al añadir usuarios al grupo
    
    add_to_registered.short_description = "Añadir usuarios al grupo 'Registered'"  # Descripción de la acción
    
    def add_to_collaborators(self, request, queryset): # Añade usuarios al grupo 'Collaborators'
        collaborators_group, created = Group.objects.get_or_create(name='Collaborators')  # Obtiene el grupo 'Collaborators'
        for user in queryset:
            user.groups.add(collaborators_group)
        self.message_user(request, "Usuarios añadidos al grupo 'Collaborators'")  # Mensaje de éxito al añadir usuarios al grupo
    
    add_to_collaborators.short_description = "Añadir usuarios al grupo 'Collaborators'"  # Descripción de la acción

    def add_to_admins(self, request, queryset):
        admin_group, created = Group.objects.get_or_create(name='Admin')  # Obtiene el grupo 'Admin'
        for user in queryset:
            user.groups.add(admin_group)
        self.message_user(request, "Usuarios añadidos al grupo 'Admin'")  # Mensaje de éxito al añadir usuarios al grupo

    add_to_admins.short_description = "Añadir usuarios al grupo 'Admin'"  # Descripción de la acción

    def remove_to_registered(self, request, queryset):
        registered_group = Group.objects.get(name='Registered')  # Obtiene el grupo 'Registered'
        for user in queryset:
            user.groups.remove(registered_group)
        self.message_user(request, "Usuarios eliminados del grupo 'Registered'")

    remove_to_registered.short_description = "Eliminar usuarios del grupo 'Registered'"  # Descripción de la acción

    def remove_to_collaborators(self, request, queryset):
        collaborators_group = Group.objects.get(name='Collaborators')  # Obtiene el grupo 'Collaborators'
        for user in queryset:       
            user.groups.remove(collaborators_group)
        self.message_user(request, "Usuarios eliminados del grupo 'Collaborators'")

    remove_to_collaborators.short_description = "Eliminar usuarios del grupo 'Collaborators'"  # Descripción de la acción

    def remove_to_admins(self, request, queryset):
        admin_group = Group.objects.get(name='Admin')  # Obtiene el grupo 'Admin'
        for user in queryset:
            user.groups.remove(admin_group)
        self.message_user(request, "Usuarios eliminados del grupo 'Admin'")

    remove_to_admins.short_description = "Eliminar usuarios del grupo 'Admin'"  # Descripción de la acción

    list_display = ('username', 'email', 'is_staff', 'is_registered', 'is_colaborator', 'is_admin', 'is_superuser')  # Campos a mostrar en la lista de usuarios

    actions = [add_to_registered,
               add_to_admins,
               add_to_collaborators,
               remove_to_registered,
               remove_to_admins,
               remove_to_collaborators,
               ]  # Añade la acción personalizada al administrador

admin.site.register(User, CustomUserAdmin)   #registro el modelo User en el admin
