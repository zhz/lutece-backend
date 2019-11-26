from annoying.functions import get_object_or_None
from django import forms

from reply.constant import MAX_CONTENT_LENGTH
from reply.models import BaseReply


class BaseReplyForm(forms.Form):
    content = forms.CharField(required=True, max_length=1024)
    parent = forms.IntegerField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        parent = cleaned_data.get('parent')
        # If this reply have parent, check it
        if parent:
            par = get_object_or_None(BaseReply, pk=parent)
            if par is None:
                self.add_error('parent', 'Unknown reply parent node')


class UpdateBaseReplyForm(forms.Form):
    pk = forms.IntegerField(required=True)
    content = forms.CharField(max_length=MAX_CONTENT_LENGTH)

    def clean(self) -> dict:
        cleaned_data = super().clean()
        pk = cleaned_data.get('pk')
        if pk and not get_object_or_None(BaseReply, pk=pk):
            self.add_error("pk", "No such reply")
        return cleaned_data


class CreateCommentReplyForm(forms.Form):
    parent = forms.IntegerField(required=True)
    content = forms.CharField(max_length=MAX_CONTENT_LENGTH)

    def clean(self) -> dict:
        cleaned_data = super().clean()
        parent = cleaned_data.get('parent')
        reply = get_object_or_None(BaseReply, pk=parent)
        if parent and (not reply or reply.disabled):
            self.add_error("parent", "No such reply")
        if reply.ancestor:
            self.add_error("parent", "Nested reply is not supported")


class ToggleReplyVoteForm(forms.Form):
    pk = forms.IntegerField(required=True)

    def clean(self) -> dict:
        cleaned_data = super().clean()
        pk = cleaned_data.get('pk')
        if pk and not get_object_or_None(BaseReply, pk=pk):
            self.add_error("pk", "No such reply")
        return cleaned_data
