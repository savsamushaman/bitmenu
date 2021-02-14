import os
from pathlib import Path

import qrcode
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from accounts.models import CustomUser


@receiver(post_save, sender=CustomUser)
def generate_qr_code(sender, instance, created, **kwargs):
    if created:
        input_data = f'http://127.0.0.1:8000/menu/{instance.username}'
        qr_code = qrcode.QRCode(version=1,
                                box_size=10,
                                border=5)
        qr_code.add_data(input_data)
        qr_code.make(fit=True)
        img = qr_code.make_image(fill='black', back_color='white')
        path = f'..\\media\\qr'
        Path(path).mkdir(exist_ok=True)
        img.save(f'{path}\\{instance.username}.png')
        instance.qr_code = f'{path}\\{instance.username}.png'
        instance.save()


@receiver(pre_delete, sender=CustomUser)
def delete_qr_code(sender, instance, **kwargs):
    if os.path.isfile(instance.qr_code.path):
        os.remove(instance.qr_code.path)
