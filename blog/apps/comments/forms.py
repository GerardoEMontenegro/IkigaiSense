from apps.post.models import Comment
from django import forms




class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escribí un comentario...'}),
        }
        labels = {
            'content': ''
        }