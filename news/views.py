from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import View

from .models import Post, Author, User, PostCategory, Category, CategorySubscribe
from .filters import NewsFilter
from .forms import PostForm

from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.db.models.signals import post_save
from django.db.models.signals import m2m_changed
from django.shortcuts import redirect, get_object_or_404, render


class NewsList(ListView):
    model = Post
    ordering = '-date'
    template_name = 'news.html'
    context_object_name = 'news'
    author ='author'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter (self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_quantity'] = len(Post.objects.all())
        return context

    def post_search(request):
        f = PostSearch(request.GET,
                       queryset=Post.objects.all())
        return render(request,
                      'search.html',
                      {'filter': f})

class NewsDetail(DetailView):
    model = Post
    ordering = '-creation_time'
    template_name = 'news_id.html'
    context_object_name = 'post'


class NewsSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'
    ordering = ['-date']



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context

class CreatePost(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'edit_post.html'
    form_class = PostForm
    permission_required = ('news.add_post',)
    model = Post
    success_url = '/news/'

    def form_valid(self, form):
        post = form.save(commit = False)
        id = post.id
        return super().form_valid(form)


class EditPost(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
  template_name = 'edit_post.html'
  form_class = PostForm
  permission_required = ('news.change_post',)
  success_url = '/news/'

  def get_object(self, **kwargs):
    id = self.kwargs.get('pk')
    return Post.objects.get(pk=id)



class DeletePost(DeleteView):
  template_name = 'delete_post.html'
  queryset = Post.objects.all()
  success_url = '/news/'



class ProtectedView(LoginRequiredMixin, TemplateView):
    template_name = 'prodected_page.html'

@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')

class CategoriesView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, 'categories.html', {'categories': Category.objects.all()})

class CategoryDetail(LoginRequiredMixin, DetailView):

    model = Category
    template_name = 'category.html'
    context_object_name = 'category'


def subscribe_to_category(request, pk):

    current_user = request.user
    CategorySubscribe.objects.create(category=Category.objects.get(pk=pk), subscriber=User.objects.get(pk=current_user.id))

    return render(request, 'subscribe.html')


def notify_new_post_in_category(sender, instance, action, **kwargs):
    if action == 'post_add':
        subscribed_users = []
        for category_subscribe in CategorySubscribe.objects.filter(category__in=instance.categories.all()):
            subscribed_users.append(category_subscribe.subscriber.email)

        send_mail(
            subject='Здравствуй. Новая статья в твоём любимом разделе!',
            html_message=render_to_string('new_post.html',
                                        context={'post': instance,
                                               'link': f'http://127.0.0.1:8000/news/{instance.id}'}),


            message="Hello",
            from_email='egorovarturxx@gmail.com',
            recipient_list=subscribed_users,
            fail_silently=False
        )
        pass

m2m_changed.connect(notify_new_post_in_category, sender=Post.categories.through)

post_save.connect(notify_new_post_in_category, sender=Post)