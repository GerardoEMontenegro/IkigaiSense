from django import forms
from apps.post.models import Post, Comment, PostImage, Category

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'allow_comments']
        labels = {
            'title': 'Título',
            'content': 'Contenido',
            'category': 'Categoría',
            'allow_comments': 'Permitir comentarios'
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Título del post', 'class': 'p-2'}),
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Escribe el contenido del post aquí...', 'class': 'p-2'}),
            'allow_comments': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        category = forms.ModelChoiceField(
                queryset=Category.objects.all(),
                empty_label="Selecciona una categoría",
                widget=forms.Select(attrs={
                    'class': 'block w-full rounded border-gray-300 shadow-sm focus:ring focus:ring-indigo-300 focus:ring-opacity-50'
                })
            )

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

    def save(self, commit=True):
        post = super().save(commit=False)
        image = self.cleaned_data.get('image')

        if commit:
            post.save()
            if image:
                # Si ya hay una imagen, actualizarla (puedes ajustarlo según tu modelo)
                PostImage.objects.update_or_create(post=post, defaults={'image': image})
        return post

class PostFilterForm(forms.Form):
    search_query = forms.CharField(
        required=False,
        label="Buscar",
        widget=forms.TextInput(attrs={
            'placeholder': 'Buscar ',
            'class': 'w-full p-2'
        })
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label='Todas las categorías',
        widget=forms.Select(attrs={'class': 'w-full p-2'})
    )

    order_by = forms.ChoiceField(
        required=False,
        label="Ordenar por",
        choices=(
            ('-created_at', 'Más recientes'),
            ('created_at', 'Más antiguos'),
            ('title', 'Título A-Z'),
            ('-title', 'Título Z-A'),
            ('-comments_count', 'Más comentados'),
        ),
        widget=forms.Select(attrs={'class': 'w-full p-2'})
    )

    fecha_publicacion = forms.DateField(
        required=False,
        label="Fecha de publicación",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full p-2'
        })
    )

    comentarios_min = forms.IntegerField(
        required=False,
        min_value=0,
        label="Mínimo comentarios",
        widget=forms.NumberInput(attrs={
            'placeholder': 'Comentarios mínimos',
            'class': 'w-full p-2'
        })
    )

    comentarios_max = forms.IntegerField(
        required=False,
        min_value=0,
        label="Máximo comentarios",
        widget=forms.NumberInput(attrs={
            'placeholder': 'Comentarios máximos',
            'class': 'w-full p-2'
        })
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
                    'rows': 3, # Número de filas del área de texto
                    'placeholder': 'Escribe tu comentario...', # Texto que aparece cuando el área de texto está vacía
                    'class': 'p-2',# Clase CSS para aplicar estilos al área de texto
                    
                }
            )
        }