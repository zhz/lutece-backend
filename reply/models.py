from django.db import models
from django.utils import timezone

from record.models import DetailedRecord
from reply.constant import MAX_CONTENT_LENGTH
from user.models import User


class BaseReply(models.Model):
    content = models.CharField(max_length=MAX_CONTENT_LENGTH, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    reply = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, db_index=True, related_name='reply_node')
    ancestor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, db_index=True,
                                 related_name='ancestor_node')
    create_time = models.DateField(default=timezone.now)
    disabled = models.BooleanField(default=False, db_index=True)
    create_time = models.DateTimeField(default=timezone.now)
    last_update_time = models.DateTimeField(default=timezone.now)
    vote = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.last_update_time = timezone.now()
        super().save(*args, **kwargs)


class ReplyVote(DetailedRecord):
    attitude = models.BooleanField(default=False)
    reply = models.ForeignKey(BaseReply, on_delete=models.SET_NULL, null=True)
