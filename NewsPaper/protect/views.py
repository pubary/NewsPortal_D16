import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from news.models import Author, Category, Post


logger = logging.getLogger('testLogger')

class UserAccountView(LoginRequiredMixin, TemplateView):
    template_name = 'user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мой аккаунт'
        context['is_not_in_authors'] = not self.request.user.groups.filter(name='authors').exists()
        user = self.request.user
        context['user'] = user
        context['categories'] = Category.objects.filter(subscribers__username=user)
        if not context['is_not_in_authors']:
            context['is_author'] = Post.objects.filter(author__author_acc=user).values('id')
            if context['is_author']:
                current_author = Author.objects.get(author_acc=self.request.user)
                context['rating'] = current_author.rating
                context['quantity'] = Post.objects.filter(author=current_author).count()
        logger.info(f'<User id {user.pk} came to his page>')
        return context


