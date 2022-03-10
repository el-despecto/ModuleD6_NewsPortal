
from datetime import datetime

from django.shortcuts import render, redirect
from django.views import View

from news.models import PostCategory, Post
from .models import Appointment

class AppointmentView(View):
    # получаем шаблон для ввода данных (make_appointment.html)
    def get(self, request, ):
        return render(request, 'make_appointment.html', {})

    # отправляем на сервер нашу информацию и сохраняем ее в БД (сохраняем новый объект класса)
    def post(self, request, ):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()

        # переход на данную форму (представление) после выполнения кода
        return redirect('make_appointment')  # (1)
