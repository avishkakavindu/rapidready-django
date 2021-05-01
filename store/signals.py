import os

from django.db.models import signals
from django.contrib.auth.models import Group
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import Stock, Material, User


@receiver(pre_save, sender=Stock)
def add_material(sender, instance, **kwargs):
    """ On insertion of new stock update materials """

    if instance._state.adding:  # upon addition
        quantity = Material.objects.get(id=instance.material.id)
        quantity.available_unit = quantity.available_unit + instance.quantity
        quantity.save()
    else:   # upon removal
        quantity = Material.objects.get(id=instance.material.id)
        diff = Stock.objects.get(id=instance.id).quantity - instance.quantity   # how much added or removed
        quantity.available_unit = quantity.available_unit - diff
        quantity.save()
        

@receiver(post_delete, sender=Stock)
def remove_material(sender, instance, *args, **kwargs):
    """ Upon deletion of stock """

    quantity = Material.objects.get(id=instance.material.id)
    quantity.available_unit = quantity.available_unit - instance.quantity
    quantity.save()


@receiver(pre_save, sender=User)
def delete_old_file(sender, instance, **kwargs):
    """ removes old profile pic """
    if instance._state.adding and not instance.pk:
        return False

    try:
        old_profile_pic = sender.objects.get(pk=instance.pk).profile_pic
    except sender.DoesNotExist:
        return False

    # comparing the new file with the old one
    new_profile_pic = instance.profile_pic
    if not old_profile_pic == new_profile_pic:
        if os.path.isfile(old_profile_pic.path):
            os.remove(old_profile_pic.path)


# @receiver(pre_save, sender=User)
# def assign_group(sender, instance, **kwargs):
    # """ Assign to a groups based on role """
    # if instance._state.adding is True:
    #     group = Group.objects.get(name=instance.get_role_display().lower())
    #     print('\n\nadding lol', group)
    #     instance.groups.add(group)
    # else:
    #     group = Group.objects.get(name=instance.get_role_display().lower())
    #     print('\n\nlol', group)
    #     group.user_set.add(instance)
    #     print('\n\n', instance.get_role_display(), '\n\n')
    #
    # # group = Group.objects.get(name=)
