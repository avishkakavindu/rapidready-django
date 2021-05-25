import os
from django.contrib import messages
from django.contrib.sites.models import Site
from django.db.models.signals import pre_save, post_delete, post_save, pre_delete
from django.dispatch import receiver
from .models import Stock, Material, User, Quote
from .util import Util


def send_notify_email(reciever, username, email_body, object_path, link_text, reason, subject):
    """ sends notify email """

    site = Site.objects.get_current().domain
    domain = site.split('/')[2]

    payload = {
        'receiver': reciever,
        'email_body': {
            'username': username,
            'email_body': email_body,
            'link': '{}{}'.format(site, object_path),
            'link_text': link_text,
            'email_reason': '{} {}'.format(reason, domain),
            'site_name': domain
        },
        'email_subject': subject,
    }

    Util.send_email(payload)


@receiver(pre_save, sender=Stock)
def add_material(sender, instance, **kwargs):
    """ On insertion of new stock update materials """

    if instance._state.adding:  # upon addition
        quantity = Material.objects.get(id=instance.material.id)
        quantity.available_unit = quantity.available_unit + instance.quantity
        quantity.save()
    else:  # upon removal
        quantity = Material.objects.get(id=instance.material.id)
        diff = Stock.objects.get(id=instance.id).quantity - instance.quantity  # how much added or removed
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


@receiver(post_save, sender=Quote)
def send_quotation(sender, instance, **kwargs):
    """ sends email upon quotation approval """

    if instance.is_possible:
        customer = instance.customer
        email_body = 'Please follow the link to view the quotation.'
        object_path = 'checkout'
        link_text = 'Please follow the link'
        reason = "You're receiving this email because you place a quote request on"
        subject = 'Your quotation is ready'

        send_notify_email(customer.email, customer.username, email_body, object_path, link_text, reason, subject)


@receiver(pre_delete, sender=Quote, dispatch_uid='quote_delete_signal')
def send_quotation_canceled(sender, instance, **kwargs):
    """ sends email upon rejected quote deletion """

    if instance.is_possible is None or not instance.is_possible:
        customer = instance.customer
        email_body = 'Sorry to inform you that requested services cannot be provided.'\
                'Here by rejecting your quote,\n "{}".'.format(instance.desc)
        object_path = ''
        link_text = 'Visit RapidReady'
        reason = "You're receiving this email because your placed quote request being rejected"
        subject = 'Your quote has being rejected'

        send_notify_email(customer.email, customer.username, email_body, object_path, link_text, reason, subject)

