from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404
from django.views.generic import View, DeleteView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import F, Value, Q, Max, Sum, Subquery, OuterRef
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from SimpleKB.knowledgebase.models import Article
from .forms import NewMessageForm
from .models import Message

USER_MODEL = get_user_model()

# Create your views here.
class DashboardView(View):
    template_name = 'social/dashboard.html'

    def get(self, request, *args, **kwargs):
        username = kwargs.pop('username', None)
        dasboard_user = get_user_model().objects.get(username=username)
        recent_articles = (Article
                           .objects
                           .filter(author=dasboard_user,
                                   article_status_id=Article.Article_Status.PUBLISHED
                                   )
                           .order_by('-updated_on')[:5]
                           )
        return render(request, self.template_name, {
            'dashboard_user': dasboard_user,
            'recent_articles': recent_articles})


class MessagesView(ListView):
    template_name = 'social/messages.html'
    model = Message
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(Q(sender=self.request.user) | Q(recipient=self.request.user))
        queryset = queryset.order_by('conversation_id', '-message_sent_date')
        queryset = queryset.select_related('sender').select_related('recipient')
        queryset = queryset.distinct('conversation_id')
        return queryset


class NewMessageView(View):
    template_name = 'social/new_message.html'

    def get(self, request):
        message_form = NewMessageForm(user=request.user)
        return render(request, self.template_name, {'message_form': message_form})

    def post(self, request):
        message_form = NewMessageForm(request.POST, user=request.user)
        if message_form.is_valid():
            message_form.save()
            messages.success(request, 'Message sent successfully!')
            recipient = message_form.cleaned_data['recipient']
            return redirect('social:message_detail', recipient.username)
        return render(request, self.template_name, {'message_form': message_form})


class MessageDetailView(View):
    template_name = 'social/message_detail.html'

    def get(self, request, username):
        user = get_object_or_404(USER_MODEL, username=username)
        return render(request, self.template_name, {'user': user})
