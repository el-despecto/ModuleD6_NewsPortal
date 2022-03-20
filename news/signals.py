from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.shortcuts import redirect
from django.template.loader import render_to_string

from .models import Post, Category


@receiver(post_save, sender=Post)
def send_sub_mail(sender, instance, created, **kwargs):

    global subscriber
    sub_text = instance.text
    category = Category.objects.get(pk=Post.objects.get(pk=instance.pk).category.pk)
    print()
    print('category:', category)
    print()
    subscribers = category.subscribers.all()

    post = instance

    print('Адреса рассылки:')
    for msg in subscribers:
        print(msg.email)

    print()
    print()
    for subscriber in subscribers:
        print(subscriber.email)

        html_content = render_to_string(
            'message_send.html', {'user': subscriber, 'text': sub_text[:50], 'post': post})

        msg = EmailMultiAlternatives(
            subject=f'Здравствуйте, {subscriber.username}. Новая статья в вашем разделе!',
            from_email='d3spector@yandex.ru',
            to=[subscriber.email]
        )

        msg.attach_alternative(html_content, 'text/html')
        print()
        print(html_content)
        print()
        msg.send()

    return redirect('/news/')
