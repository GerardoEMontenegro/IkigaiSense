from django import forms
from apps.post.models import Post, Comment, PostImage, Category

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'allow_comments']
        labels = {
            'title': 'Título',
            'content': 'Contenido',
            'allow_comments': 'Permitir comentarios'
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Título del post', 'class': 'p-2'}),
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Escribe el contenido del post aquí...', 'class': 'p-2'}),
            'allow_comments': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

class PostCreateForm(PostForm):
    image = forms.ImageField(required=False)

    def save(self, commit=True):
        post = super().save(commit=False)
        image = self.cleaned_data.get('image')

        if commit:
            post.save()
            if image:
                PostImage.objects.create(post=post, image=image)
        return post
    
class PostUpdateForm(PostForm):
    pass

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


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment

        fields = ['content']

        labels = {
            'content':  'Comentario'
        }

        widgets = {
            'content': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Escribe tu comentario...',
                    'class': 'p-2',
                    
                }
            )
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title']  # Asegúrate de que 'name' es un campo de tu modelo Category
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500',
                'placeholder': 'Introduce el nombre de la categoría'
            })
        }