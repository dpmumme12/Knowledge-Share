from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from ..forms import ArticleForm, ArticleUserForm
from ..models import Article, ArticleImage


class ArticleView(View):
    template_name = 'knowledgebase/article_view.html'
    article_user_form = ArticleForm

    def get(self, request, **kwargs):
        article_id = kwargs.pop('article_id', None)
        article_user_form = None
        article = (Article
                   .objects
                   .filter(id=article_id)
                   .select_related('author')
                   .get()
                   )
        if request.user.is_authenticated:
            article_user_form = ArticleUserForm(user=request.user,
                                                initial={'article': article,
                                                         'user': request.user})
        return render(request, self.template_name, {
            'article': article,
            'ArticleUserForm': article_user_form
        })

    def post(self, request, **kwargs):
        article_id = kwargs.pop('article_id', None)
        article_user_form = ArticleUserForm(request.POST, user=request.user)
        if article_user_form.is_valid():
            article_user_form.save()
            messages.success(request, 'Article added to knowledgebase!')
        else:
            messages.error(request, article_user_form.errors.as_json(escape_html=True))

        return redirect('knowledgebase:article', article_id=article_id)


class ArticleEditView(LoginRequiredMixin, View):
    template_name = 'knowledgebase/article_edit.html'

    def get(self, request, article_id=None):

        # Creates new article if no id is supplied
        if article_id is None:
            article = Article.objects.create(
                author=request.user,
                article_status_id=Article.Article_Status.DRAFT,
                version_status_id=Article.Version_Status.ACTIVE
            )
            return redirect('knowledgebase:article_edit', article_id=article.id)

        current_article = get_object_or_404(Article, id=article_id, author=request.user)
        article_versions = (Article
                            .objects
                            .filter(uuid=current_article.uuid)
                            .order_by('-id')
                            )
        return render(request, self.template_name, {
            'ArticleForm': ArticleForm(user=request.user, instance=current_article),
            'article_versions': article_versions,
            'article': current_article,
        })

    def post(self, request, article_id):
        """
        Updates an article instance and takes extra
        actions if a submit_type is supllied.

        Submit types:
        1. New_Version: Creates new version of the article.
        2. Publish: Publishes the article.
        """

        article = get_object_or_404(Article, id=article_id, author=request.user)
        form = ArticleForm(request.POST, user=request.user, instance=article)
        submit_type = request.POST['SubmitButton']

        if submit_type:
            submit_type = int(submit_type)

        if submit_type == Article.Version_Status.NEW_VERSION:
            new_version = article.create_new_version()
            messages.info(request, 'New version created')
            return redirect('knowledgebase:article_edit', article_id=new_version.id)

        if form.is_valid():
            form.save()
            if submit_type == Article.Article_Status.PUBLISHED:
                article.publish_article()
                messages.success(request, 'Article published successfully!')
            else:
                messages.success(request, 'Article saved successfully!')
            return redirect('knowledgebase:kb', username=request.user.username)
        else:
            return render(request, self.template_name, {
                'ArticleForm': form,
                'article': article})


class ArticleDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Article
    success_message = 'Article deleted successfully!'

    def form_valid(self, form):
        self.object = self.get_object()
        success_url = self.get_success_url()

        # If deleting active version for article.
        # Deletes all versions as well
        if self.object.version_status_id == Article.Version_Status.ACTIVE:
            Article.objects.filter(uuid=self.object.uuid).delete()
        else:
            self.object.delete()

        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return reverse_lazy('knowledgebase:kb', kwargs={'username': self.request.user.username})


class ArticleImageUploadView(LoginRequiredMixin, View):
    def post(self, request):
        if 'file' in request.FILES:
            article = (Article
                       .objects
                       .get(id=request.POST['article_id'])
                       )
            image = ArticleImage.objects.create(
                article_id=article,
                image=request.FILES['file']
            )
            return JsonResponse({'location': image.image.url})
        else:
            return JsonResponse('No image found', safe=False)


class RemoveForeignArticleView(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        article_id = kwargs.pop('article_id', None)
        article = get_object_or_404(Article, id=article_id)
        article.foreign_users.remove(request.user)
        messages.success(request, 'Article removed from knowledgebase!')

        # Redirects back to the url that mad ethe request
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
