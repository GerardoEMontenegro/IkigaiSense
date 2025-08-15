from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from apps.user.models import User


class CustomUserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('alias', 'avatar')}),
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'alias', 'avatar', 'password1', 'password2')
        }),
    )

    def is_registered(self, obj):
        return obj.groups.filter(name='Registered').exists()
    is_registered.short_description = 'Es Usuario Registrado'
    is_registered.boolean = True

    def is_collaborator(self, obj):
        return obj.groups.filter(name='Collaborator').exists()
    is_collaborator.short_description = 'Es Colaborador'
    is_collaborator.boolean = True

    def is_admin(self, obj):
        return obj.groups.filter(name='Admin').exists()
    is_admin.short_description = 'Es Administrador'
    is_admin.boolean = True

    def add_to_registered(self, request, queryset):
        registered_group = Group.objects.get(name='Registered')
        for user in queryset:
            user.groups.add(registered_group)
        self.message_user(
            request, "Los usuarios seleccionados fueron añadidos al grupo 'Registered'.")
    add_to_registered.short_description = 'Agregar a Usuarios Registrados'

    def add_to_collaborator(self, request, queryset):
        collaborator_group = Group.objects.get(name='Collaborator')
        for user in queryset:
            user.groups.add(collaborator_group)
        self.message_user(
            request, "Los usuarios seleccionados fueron añadidos al grupo 'Collaborator'.")
    add_to_collaborator.short_description = 'Agregar a Colaboradores'

    def add_to_admin(self, request, queryset):
        admin_group = Group.objects.get(name='Admin')
        for user in queryset:
            user.groups.add(admin_group)
        self.message_user(
            request, "Los usuarios seleccionados fueron añadidos al grupo 'Admin'.")
    add_to_admin.short_description = 'Agregar a Administradores'

    def remove_from_registered(self, request, queryset):
        registered_group = Group.objects.get(name='Registered')
        for user in queryset:
            user.groups.remove(registered_group)
        self.message_user(
            request, "Los usuarios seleccionados fueron removidos del grupo 'Registered'.")
    remove_from_registered.short_description = 'Remover de Usuarios Registrados'

    def remove_from_collaborator(self, request, queryset):
        collaborator_group = Group.objects.get(name='Collaborator')
        for user in queryset:
            user.groups.remove(collaborator_group)
        self.message_user(
            request, "Los usuarios seleccionados fueron removidos del grupo 'Collaborator'.")
    remove_from_collaborator.short_description = 'Remover de Colaboradores'

    def remove_from_admin(self, request, queryset):
        admin_group = Group.objects.get(name='Admin')
        for user in queryset:
            user.groups.remove(admin_group)
        self.message_user(
            request, "Los usuarios seleccionados fueron removidos del grupo 'Admin'.")
    remove_from_admin.short_description = 'Remover de Administradores'

    list_display = ('username', 'email', 'is_staff', 'is_superuser',
                    'is_registered', 'is_collaborator', 'is_admin')

    actions = [
        add_to_registered,
        add_to_collaborator,
        add_to_admin,
        remove_from_registered,
        remove_from_collaborator,
        remove_from_admin,
    ]


admin.site.register(User, CustomUserAdmin)