from django import forms
from apps.post.models import Post, Comment, PostImage

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'content', 'allow_comments']  
        labels = {
            'title': 'Título',
            'category': 'Categorías',  
            'content': 'Contenido',
            'allow_comments': 'Permitir comentarios',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#6D9773]'
            }),
            'category': forms.Select(attrs={  
                'class': 'form-select w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#6D9773]',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-textarea w-full px-4 py-2 border border-gray-300 rounded-lg',
                'rows': 8
            }),
            'allow_comments': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-5 w-5 text-[#6D9773] rounded focus:ring-[#6D9773]'
            }),
        }



class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ['id', 'image']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-file w-full px-4 py-2 border border-gray-300 rounded-lg',
            })
        }

ImageFormSet = forms.inlineformset_factory(
    Post,
    PostImage,
    form=PostImageForm,
    extra=3,        # Muestra 3 campos vacíos para subir imágenes
    can_delete=True,
    max_num=5,
    validate_max=True,
)

class PostFilterForm(forms.Form):
    search_query = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Buscar...',
                   'class': 'w-full p-2 bg-red-200'}
        )
    )
    order_by = forms.ChoiceField(
        required=False,
        choices=(
            ('-created_at', 'Más recientes'),
            ('created_at', 'Más antiguos'),
            ('-comments_count', 'Más comentados')),
       
        widget=forms.Select(
            attrs={'class': 'w-full p-2'}
        )
    )