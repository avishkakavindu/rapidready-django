from django.core.management import BaseCommand
from django.contrib.auth.models import User, Group, Permission
import logging

GROUPS = {
    'production manager': {
        # django app model specific permissions
        "order": ['add', 'change', 'delete', 'view'],
        "ordered service": ['add', 'change', 'delete', 'view'],
        "service material": ['add', 'change', 'delete', 'view'],
        "service": ['add', 'change', 'delete', 'view'],
        "category": ['add', 'change', 'delete', 'view'],
        "cart": ['add', 'change', 'delete', 'view'],
        "cart item": ['add', 'change', 'delete', 'view'],
        "review": ['add', 'change', 'delete', 'view'],
        "quote": ['add', 'change', 'delete', 'view'],
    },
    'production team': {
        "order": ['change','view'],
        "ordered service": ['view'],
    },
    'store manager': {
        "stock": ['add', 'change', 'delete', 'view'],
        "material": ['add', 'change', 'delete', 'view'],
    },
    'store team': {
        "stock": ['change','view'],
        "material": ['change', 'view'],
    },
    'supplier':{
        "stock": ['view'],
    }
}


class Command(BaseCommand):
    """
    Programmatic Group and Permission creation
    >>> python manage.py create_groups
    """

    help = 'Creates read only default permission groups for users'

    def handle(self, *args, **kwargs):
        for group in GROUPS:
            new_group, crated = Group.objects.get_or_create(name=group)

            # iterate through models in group
            for model in GROUPS[group]:
                # iterate through permissions
                for permission in GROUPS[group][model]:
                    # Generate permission name as Django would generate it
                    name = "Can {} {}".format(permission, model)
                    print("Creating {}".format(name))

                    try:
                        model_add_perm = Permission.objects.get(name=name)
                    except Permission.DoesNotExist:
                        logging.warning("Permission not found with name '{}'".format(name))
                        continue

                    new_group.permissions.add(model_add_perm)

