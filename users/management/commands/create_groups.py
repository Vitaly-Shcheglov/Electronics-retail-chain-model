from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from users.models import CustomUser


class Command(BaseCommand):
    """
    Команда для создания групп с определенными разрешениями.
    """

    help = "Create groups with specific permissions"

    def handle(self, *args, **kwargs):
        """
        Выполняет команду для создания группы и назначения разрешений.
        """
        network_moderator_group, created = Group.objects.get_or_create(name="Network moderator group")
        can_view_users = Permission.objects.get(codename="can_view_users")
        can_block_user = Permission.objects.get(codename="can_block_user")

        network_moderator_group.permissions.add(
            can_view_users,
            can_block_user,
        )

        user = CustomUser.objects.get(
            phone_number="89090249875"
        )  # Замените на фактический phone_number зарегистрированного пользователя

        user.groups.add(network_moderator_group)

        self.stdout.write(self.style.SUCCESS("Successfully created groups and assigned permissions."))
