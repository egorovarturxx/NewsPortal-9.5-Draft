from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.mail import EmailMultiAlternatives
from datetime import datetime

from django.template.loader import render_to_string
from .models import Appointment

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_managers


def notify_managers_appointment(sender, instance, created, **kwargs):
    subject = f'{instance.client_name} {instance.date.strftime("%d %m %Y")}'

    mail_managers(
        subject=subject,
        message=instance.message,
    )

post_save.connect(notify_managers_appointment, sender=Appointment)



class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()

        html_content = render_to_string(
            'appointment_created.html',
            {
                'appointment': appointment,
            }
        )


        msg = EmailMultiAlternatives(
            subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
            body=appointment.message,
            from_email='egorovarturxx@gmail.com',
            to=['egorovarturxx@gmail.com'],
        )
        msg.attach_alternative(html_content, "text/html")

        msg.send()

        return redirect('appointment:make_appointment')