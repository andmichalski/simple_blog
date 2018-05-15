from django.forms import ModelForm
from django import forms
from blog.models import Comment

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'author']
        widgets = {
          'text': forms.Textarea(attrs={'rows':1, 'cols':40}),
        }
