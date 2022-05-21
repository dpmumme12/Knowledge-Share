from django.db import models
from django.conf import settings
from django.urls import reverse
from SimpleKB.utils.models import TimeStampedModel

# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.SET_NULL,
                               null=True,
                               related_name='sender')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  related_name='recipient')
    content = models.TextField()
    message_sent_date = models.DateTimeField(auto_now=True)
    message_read = models.BooleanField(default=False)
    conversation_id = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        min_id = min(self.sender.id, self.recipient.id)
        max_id = max(self.sender.id, self.recipient.id)
        self.conversation_id = str(min_id) + '-' + str(max_id)

        url = reverse('social:message_detail', args=(self.sender.username,))
        Notification.objects.create(message=f"""
                                    New message from
                                    <a href="{url}"class="text-decoration-none">
                                    @{self.sender.username}</a>
                                    """,
                                    user=self.recipient)
        super(Message, self).save(*args, **kwargs)


class Notification(TimeStampedModel):
    message = models.CharField(max_length=300)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
