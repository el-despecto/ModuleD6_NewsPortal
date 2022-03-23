Настроено приветственное письмо, которое отправляется пользователю при регистрации: appointment/templates/account/email/email_confirmation_signup_message.html
и текст приветствие: appointment/templates/account/email/email_confirmation_subject.txt
В settings.py добавлены настройки django-allauth
urls.py: ссылки на авторизацию     path('accounts/', include('allauth.urls'))

Добавлена возможность подписываться на категорию новостей, для этого в news\models.py для класа Category добавлено поле   subscribers = models.ManyToManyField(User, ).
Views.py добавлена функция подписки def add_subscribe(request, **kwargs)с возможностью проверить в терминале проходит ли подписка на выбранную категорию   print(request.user, ' подписан на обновления категории:', Category.objects.get(pk=pk))
а также функция отписки от категории def del_subscribe(request, **kwargs)


При добавлении новой статьи подписчикам отправляется рассылка с помошью планировщика задач appointments\management\commands\runapscheduler.py
Реализована возможность рассылки писем еженедельно с новыми статьями, добавленными за неделю в разделе, на который подписан пользователь  # trigger=CronTrigger(day_of_week="mon", hour="08", minute="00"),
 