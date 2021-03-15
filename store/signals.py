from django.db.models import signals
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import Stock, Material


@receiver(pre_save, sender=Stock)
def addmaterial(sender, instance, **kwargs):
    # on insertion of new stock
    if instance._state.adding:
        quantity = Material.objects.get(id=instance.material.id)
        quantity.available_unit = quantity.available_unit + instance.quantity
        quantity.save()
    # on updating of stock
    else:
        quantity = Material.objects.get(id=instance.material.id)
        diff = Stock.objects.get(id=instance.id).quantity - instance.quantity   # how much added or removed
        quantity.available_unit = quantity.available_unit - diff
        quantity.save()
        

@receiver(post_delete, sender=Stock)
def removematerial(sender, instance, *args, **kwargs):
    quantity = Material.objects.get(id=instance.material.id)
    quantity.available_unit = quantity.available_unit - instance.quantity
    quantity.save()
