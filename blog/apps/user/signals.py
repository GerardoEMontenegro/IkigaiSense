# apps/user/signals.py

from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.post.models import Post, Comment


@receiver(post_migrate)
def create_groups_and_permissions(sender, **kwargs):
    try:
        post_ct = ContentType.objects.get_for_model(Post)
        comment_ct = ContentType.objects.get_for_model(Comment)

        # Obtener permisos
        perms = {
            'post': {
                'view': Permission.objects.get(codename='view_post', content_type=post_ct),
                'add': Permission.objects.get(codename='add_post', content_type=post_ct),
                'change': Permission.objects.get(codename='change_post', content_type=post_ct),
                'delete': Permission.objects.get(codename='delete_post', content_type=post_ct),
            },
            'comment': {
                'view': Permission.objects.get(codename='view_comment', content_type=comment_ct),
                'add': Permission.objects.get(codename='add_comment', content_type=comment_ct),
                'change': Permission.objects.get(codename='change_comment', content_type=comment_ct),
                'delete': Permission.objects.get(codename='delete_comment', content_type=comment_ct),
            }
        }

        # Registered
        registered_group, _ = Group.objects.get_or_create(name='Registered')
        registered_group.permissions.set([
            perms['post']['view'],
            perms['comment']['view'],
            perms['comment']['add'],
            perms['comment']['change'],
            perms['comment']['delete'],
        ])

        # Collaborator
        collaborator_group, _ = Group.objects.get_or_create(name='Collaborator')
        collaborator_group.permissions.set([
            perms['post']['view'],
            perms['post']['add'],
            perms['post']['change'],
            perms['comment']['view'],
            perms['comment']['add'],
            perms['comment']['change'],
        ])

        # Admins
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        admin_group.permissions.set([
            perms['post']['view'],
            perms['post']['add'],
            perms['post']['change'],
            perms['post']['delete'],
            perms['comment']['view'],
            perms['comment']['add'],
            perms['comment']['change'],
            perms['comment']['delete'],
        ])

        print("✅ Grupos y permisos creados correctamente tras aplicar migraciones.")

    except Permission.DoesNotExist:
        print("❌ Algunos permisos aún no están disponibles. Asegúrate de haber aplicado todas las migraciones.")


