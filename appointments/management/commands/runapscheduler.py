import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news.models import Category, Post
from datetime import datetime

logger = logging.getLogger(__name__)


def send_mail():

    print('Проверка')

    for category in Category.objects.all():

        all_news = []
        week_number_last = datetime.now().isocalendar()[1] - 1

        for news in Post.objects.filter(category_id=category.id,
                                        dateCreation__week=week_number_last).values('pk',
                                                                                    'title',
                                                                                    'dateCreation',
                                                                                    'category_id__name'):

            date_format = news.get("dateCreation").strftime("%m/%d/%Y")

            new = (f' http://127.0.0.1:8000/news/{news.get("pk")}, {news.get("title")}, '
                   f'Категория: {news.get("category_id__name")}, Дата создания: {date_format}')

            all_news.append(new)

        print(category.name)
        print()
        print("Письма будут отправлены подписчикам категории", category.name, '( id:', category.id, ')')

        subscribers = category.subscribers.all()
        print('следующим адресам: ')
        for msg in subscribers:
            print(msg.email)

        for subscriber in subscribers:
            print(subscriber.email)
            print()
            print('Письмо, отправленное на email: ', subscriber.email)
            html_content = render_to_string(
                'message_send.html', {'user': subscriber,
                                     'text': all_news,
                                     'category_name': category.name,
                                     'week_number_last': week_number_last})

            msg = EmailMultiAlternatives(
                subject=f'Здравствуйте, {subscriber.username}, новые статьи за прошлую неделю!',
                from_email='d3spector@yandex.ru',
                to=[subscriber.email]
            )

            msg.attach_alternative(html_content, 'text/html')
            print()
            print(html_content)
            msg.send()

#
# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")


        scheduler.add_job(
            send_mail,
            trigger=CronTrigger(second="*/30"),
            # trigger=CronTrigger(day_of_week="mon", hour="08", minute="00"),
            id="send_mail",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'send_mail'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")