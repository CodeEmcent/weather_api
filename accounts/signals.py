import random
import time
import hashlib
import os
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.auth import get_user_model
from config import settings
from django.utils import timezone
from .models import *


User = get_user_model()

@receiver(post_save, sender=User)
def welcome(sender, instance, created, *args, **kwargs):
    if created:
        if instance.role == 'user':
            password = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))
            instance.set_password(password)
            instance.save()
            subject = 'Welcome to our website!'
            message = f'Dear {instance.last_name},\n\nYour password is: {password}\n\nPlease change it as soon as possible.'
            # send_mail(subject, message, 'noreply@example.com', [instance.email])
            
            print(f'Welcome email sent to {instance.first_name}')
            time.sleep(5)
            print(f'mail sent to {instance.email}')
            print(f"""
                    subject: {subject}
                    message: {message}
                """)
        else:
            print(f'User {instance.email} has been created as a {instance.role}')

# @receiver(data_signal)
# def data_signal(self, *args, **kwargs):
#     pass
