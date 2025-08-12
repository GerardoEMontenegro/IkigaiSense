from django.test import TestCase
from django.core.mail import send_mail

def test_mail():
    send_mail(
        'Prueba de correo Mailtrap',
        'Este es un correo de prueba desde Django con Mailtrap.',
        'from@example.com',
        ['to@example.com'],
        fail_silently=False,
    )
    print("Correo enviado!")

# Create your tests here.
