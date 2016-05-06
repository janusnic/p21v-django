from django import forms
from .models import Comment, Article

class CommentForm(forms.ModelForm):
    ancestor = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'ancestor'}), required=False)
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': '65', 'rows': '6'}))
    
    class Meta:
        model = Comment
        fields = ('name', 'website', 'content',)
