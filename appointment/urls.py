from django.urls import path
from .views import AppointmentView

urlpatterns = [
path('make_appointment/', AppointmentView.as_view(), name='appointment'),
path('appointment_created/', AppointmentView.as_view()),
]