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


    
class CommentEditForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full border border-gray-300 rounded-md p-2 font-tangerine text-slate-800',
                'placeholder': 'Edita tu comentario...'
            })
        }