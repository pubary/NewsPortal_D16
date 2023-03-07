import time
import logging

from allauth.account.models import EmailAddress
from django.contrib.auth.models import User
from django.core.cache import cache
from django.shortcuts import get_object_or_404

from .models import Post, Comment
from .tasks import mail_notify_new_post


DAY_POST_LIMIT = 3


def is_limit_spent(user):
    lim = DAY_POST_LIMIT
    posts = Post.objects.filter(author__author_acc=user)
    quantity = posts.count()
    if quantity < lim:
        return False
    else:
        time_post = posts.order_by('-time').values_list('time', flat=True)[(lim-1):lim]
        dt = (time.time() - time_post[0].timestamp()) / 3600 / 24
        if dt > 1:
            return False
        else:
            return lim


def notify_new_post():
    new_post = Post.objects.all().order_by('-time').first()
    msg_data = {}
    msg_data['new_post_title'] = new_post.title
    msg_data['new_post_text'] = new_post.text[:63]
    msg_data['new_post_time'] = new_post.time
    msg_data['author_first_name'] = new_post.author.author_acc.first_name
    msg_data['author_last_name'] = new_post.author.author_acc.last_name
    msg_data['new_post_pk'] = new_post.id
    subscribers_name = set(new_post.category.values_list('subscribers__username', flat=True))
    t = 7
    print(f'Поиск подписчиков новой публикации id{new_post.id}')
    for subscriber_name in subscribers_name:
        if subscriber_name == new_post.author.author_acc.username:
            break
        if subscriber_name:
            msg_data['subscriber_name'] = subscriber_name
            subscriber_email = User.objects.get(username=subscriber_name).email
            if subscriber_email:
                print(f'Проверка валидации почты {subscriber_email}')
                if EmailAddress.objects.filter(email=subscriber_email).exists():
                    if EmailAddress.objects.get(email=subscriber_email).verified:
                        msg_data['subscriber_email'] = subscriber_email
                        print(t, ' Создание задачи уведомления для ', msg_data['subscriber_email'])
                        mail_notify_new_post.apply_async([msg_data], countdown=t)
                        t += 7


def like_dislike(request, kwargs):
    key = list(dict(request.GET.lists()).keys())[0]
    post_id = kwargs['pk']
    post = get_object_or_404(Post, id=post_id)
    if key.isalpha():
        if request.user != post.author.author_acc:
            if key == 'like':
                post.like()
            elif key == 'dislike':
                post.dislike()
    elif key.isdigit():
        comment = get_object_or_404(Comment, id=key)
        if request.user != comment.user:
            if request.GET[key] == '+':
                comment.like()
            elif request.GET[key] == '-':
                comment.dislike()
    post.author.update_rating()
    cache.delete(f'comments_to_post{post_id}')


def send_comment(request, post):
    text = request.POST['comment']
    user = request.user
    logger = logging.getLogger('testLogger')
    if len(text):
        comment = Comment(text=text, post=post, user=user)
        comment.save()
        cache.delete(f'comments_to_post{post.id}')
        comm_id = Comment.objects.filter(text=text, user=user).values_list('pk', flat=True)[0]
        logger.info(f'<User id {request.user.id} send comment id {comm_id}>')
