from django.db import models
from django.conf import settings

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
        super(Message, self).save(*args, **kwargs)
